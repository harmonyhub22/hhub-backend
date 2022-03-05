from distutils.log import debug
import os
from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, redirect, request, session, send_from_directory
from flask_restful import Api
from app.api.LoginApi import LoginApi
from app.api.LogoutApi import LogoutApi
from app.api.MatchingQueueApi import MatchingQueueApi
from app.db.db import db
from app.db.seed.data import seed
from app.api.MemberApi import MemberApi
from app.api.GenreApi import GenreApi
from app.api.LayerApi import LayerApi
from app.api.SessionApi import SessionApi, SessionEndApi, SessionLiveApi
from app.api.CommonApi import CommonApi
from app.api.SongApi import SongApi
from app.exceptions.ErrorHandler import handle_error
#from app.middleware.GoogleAuth import getOrCreateMember, getSession, login, verifyLogin
from app.middleware.NoAuth import getCookie
from app.services.MemberService import getById
from app.socket.init import sio
from flask_socketio import emit

def create_app(config_file):
    """
    Creating and returning the app
    """

    app_path = os.path.dirname(os.path.abspath(__file__))
    project_folder = os.path.expanduser(app_path)
    load_dotenv(os.path.join(project_folder, '.env'))

    app = Flask(__name__)

    # rest api
    api = Api(app)
    app.config.from_pyfile(config_file)

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

        seed()

        @app.route('/favicon.ico')
        def favicon():
            return send_from_directory(app.root_path,
                                'favicon.ico', mimetype='image/vnd.microsoft.icon')

        '''
        @app.before_request
        def authenticate():
            if request.path == '/logout': # let them logout no matter what
                return
            memberid = getSession()
            if not memberid and request.path == '/google-login': # don't check for session when google redirects
                return
            if not memberid: # check for session
                print('you must login')
                authUrl = login()
                return redirect(authUrl)
                #return jsonify({ 'url': authUrl }), 302
            if getById(memberid) == None: # the database doesn't have them so logout
                return jsonify({ 'url': authUrl }), 302
                #return redirect('/logout')
            request.environ['HTTP_MEMBERID'] = memberid
        
        @app.route('/google-login')
        def authCallback():
            if not request.args.get('state'):
                authUrl = login()
                return jsonify({ 'url': authUrl }), 302
            verifyLogin()
            getOrCreateMember()
            # return redirect(os.getenv('CORS_ORIGIN'))
            return jsonify({ 'success': True })
        '''
    
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

        @app.route('/')
        def home():
            return "<h1>Welcome to hhub backend</h1>"

        @app.errorhandler(404)
        def page_not_found(e):
            return '<h4>Route not found: ' + str(request.path) + '<h4>'

        app.register_error_handler(Exception, handle_error)

        # add all restful api routes
        api.add_resource(CommonApi, '/api/')
        api.add_resource(LoginApi, '/api/login')
        api.add_resource(LogoutApi, '/api/logout')
        api.add_resource(MemberApi, '/api/members', '/api/members/<id>')
        api.add_resource(GenreApi, '/api/genres', '/api/genres/<id>')
        api.add_resource(SessionLiveApi, '/api/session/live')
        api.add_resource(SessionApi, '/api/session', '/api/session/<id>')
        api.add_resource(SessionEndApi, '/api/session/<id>/end')
        api.add_resource(LayerApi, '/api/session/<sessionId>/layers', '/api/session/<sessionId>/layers/<id>')
        api.add_resource(MatchingQueueApi, '/api/queue', '/api/queue/<id>')
        api.add_resource(SongApi, '/api/songs', '/api/songs/<id>')

        #app.add_url_rule('/oauth', endpoint='oauth.index', view_func=oauth.index)
        #app.add_url_rule('/oauth/callback', endpoint='oauth.callback', view_func=oauth.callback)

        # Request pre and post processors
        #app.before_request(oauth.enforce_login)
        app.before_request(getCookie)

        return app, sio