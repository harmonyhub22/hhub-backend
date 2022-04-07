from distutils.log import debug
import os
from flask import Flask, jsonify, make_response, redirect, request, session, send_from_directory
from flask_restful import Api
from app.api.LogoutApi import LogoutApi
from app.api.MatchingQueueApi import MatchingQueueApi
from app.db.db import db
from app.db.seed.seedData import seed
from app.db.seed.seedTestData import seedTest
from app.api.MemberApi import MemberApi
from app.api.LayerApi import LayerApi
from app.api.SessionApi import SessionApi, SessionEndApi, SessionLiveApi
from app.api.CommonApi import CommonApi
from app.api.SongApi import SongApi
from app.api.AuthenticationAPI import AuthenticationApi
from app.exceptions.ErrorHandler import handle_error
from app.middleware.Auth import getCookie
from app.socket.init import sio
from app.controller.upload import layerUploadBlueprint

def create_app(test_config=None):
    app_path = os.path.dirname(os.path.abspath(__file__))
    project_folder = os.path.expanduser(app_path)

    app = Flask(__name__)

    # rest api
    api = Api(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('settings.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # database
    db.init_app(app)

    # sockets
    sio.init_app(app, cors_allowed_origins=os.getenv('CORS_ORIGIN'), logger=True)

    with app.app_context():

        cmd = "CREATE SCHEMA IF NOT EXISTS " + os.getenv('SCHEMA', 'public') + ";"
        db.session.execute(cmd)
        cmd = "SET search_path TO " + os.getenv('SCHEMA', 'public') + ";"
        db.session.execute(cmd)
        db.session.commit()
        
        db.create_all()
        
        if test_config is None:
            seed()
        else:
            seedTest()

        @app.route('/favicon.ico')
        def favicon():
            return send_from_directory(app.root_path,
                                'favicon.ico', mimetype='image/vnd.microsoft.icon')
    
        # CORS section
        @app.after_request
        def after_request_func(response):
            if request.method == 'OPTIONS':
                response = make_response()
                response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
                response.headers.add('Access-Control-Allow-Headers', 'x-csrf-token')
                response.headers.add('Access-Control-Allow-Methods',
                                    'GET, POST, OPTIONS, PUT, PATCH, DELETE')
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            response.headers.add('Access-Control-Allow-Origin', os.getenv('CORS_ORIGIN'))
            return response

        @app.route('/')
        def home():
            return "<h1>Welcome to hhub backend</h1>"

        @app.errorhandler(404)
        def page_not_found(e):
            return '<h4>Route not found: ' + str(request.path) + '<h4>'

        app.register_error_handler(Exception, handle_error)

        app.register_blueprint(layerUploadBlueprint)

        # add all restful api routes
        api.add_resource(CommonApi, '/api/')
        api.add_resource(AuthenticationApi, '/api/login', '/api/signup')
        api.add_resource(LogoutApi, '/api/logout')
        api.add_resource(MemberApi, '/api/members', '/api/members/<id>')
        api.add_resource(SessionLiveApi, '/api/session/live')
        api.add_resource(SessionApi, '/api/session', '/api/session/<id>')
        api.add_resource(SessionEndApi, '/api/session/<id>/end')
        api.add_resource(LayerApi, '/api/session/<sessionId>/layers', '/api/session/<sessionId>/layers/<id>')
        api.add_resource(MatchingQueueApi, '/api/queue', '/api/queue/<id>')
        api.add_resource(SongApi, '/api/songs', '/api/songs/<id>')

        # Request pre and post processors
        app.before_request(getCookie)

        return app, sio