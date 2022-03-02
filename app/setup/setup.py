import os
import socketio
from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, redirect, request, session, send_from_directory
from flask_restful import Api
from app.api.MatchingQueueApi import MatchingQueueApi
from app.db.db import db
from app.db.seed.data import seed
from app.api.MemberApi import MemberApi
from app.api.GenreApi import GenreApi
from app.api.LayerApi import LayerApi
from app.api.SessionApi import SessionApi, SessionEndApi, SessionLiveApi
from app.api.CommonApi import CommonApi
from app.exceptions.ErrorHandler import handle_error
from app.middleware.GoogleAuth import getOrCreateMember, getSession, login, verifyLogin
from flask_cors import CORS
from app.socket.init import sio



def create_app(config_file):
    """
    Creating and returning the app
    """

    app_path = os.path.dirname(os.path.abspath(__file__))
    project_folder = os.path.expanduser(app_path)
    load_dotenv(os.path.join(project_folder, '.env'))

    app = Flask(__name__)

    cors = CORS(app, resources={r"/*": {"origins": os.getenv('CORS_ORIGIN')}})

    # rest api
    api = Api(app)
    app.config.from_pyfile(config_file)

    # sockets
    app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)

    db.init_app(app)

    with app.app_context():
        db.drop_all()

        cmd = "CREATE SCHEMA IF NOT EXISTS " + os.getenv('SCHEMA', 'hhub') + ";"
        db.session.execute(cmd)
        cmd = "SET search_path TO " + os.getenv('SCHEMA', 'hhub') + ";"
        db.session.execute(cmd)
        db.session.commit()
        
        db.create_all()

        seed()

        @app.route('/favicon.ico')
        def favicon():
            return send_from_directory(app.root_path,
                                'favicon.ico', mimetype='image/vnd.microsoft.icon')
    
        @app.before_request
        def authenticate():
            memberid = getSession()
            print("The member ID is ", memberid)
            if not memberid and request.path == '/google-login':
                return
            if not memberid:
                print('you must login')
                authUrl = login()
                print("DEBUG: " + authUrl)
                return redirect(authUrl)
            request.environ['HTTP_MEMBERID'] = memberid 
        
        ### CORS section
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
        ### end CORS section

        
        @app.route('/google-login')
        def authCallback():
            if not request.args.get('state'):
                authUrl = login()
                return redirect(authUrl)
            print('auth redirect')
            verifyLogin()
            getOrCreateMember()   
            return jsonify({ 'success': True })

        @app.route('/logout')
        def logout():
            session.clear()
            return jsonify({ 'success': True })
    
        @app.route('/')
        def home():
            return "<h1>Welcome to hhub backend</h1>"

        app.register_error_handler(Exception, handle_error)

        api.add_resource(CommonApi, '/api/')
        api.add_resource(MemberApi, '/api/members', '/api/members/<id>')
        api.add_resource(GenreApi, '/api/genres', '/api/genres/<id>')
        api.add_resource(SessionLiveApi, '/api/session/live')
        api.add_resource(SessionApi, '/api/session', '/api/session/<id>')
        api.add_resource(SessionEndApi, '/api/session/<id>/end')
        api.add_resource(LayerApi, '/api/session/<sessionId>/layers', '/api/session/<sessionId>/layers/<id>')
        api.add_resource(MatchingQueueApi, '/api/queue', '/api/queue/<id>')
        
        return app