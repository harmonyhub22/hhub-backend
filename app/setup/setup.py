import os
from dotenv import load_dotenv
from flask import Flask, jsonify, redirect, request, session, send_from_directory
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



def create_app(config_file):
    """
    Creating and returning the app
    """

    app_path = os.path.dirname(os.path.abspath(__file__))
    project_folder = os.path.expanduser(app_path)
    load_dotenv(os.path.join(project_folder, '.env'))

    app = Flask(__name__)
    api = Api(app)
    
    app.config.from_pyfile(config_file)

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
            print(app.root_path)
            memberid = getSession()
            if not memberid and request.path == '/google-login':
                print('request path is /google-login')
                return
            if not memberid:
                print('you must login')
                authUrl = login()
                return redirect(authUrl)
            request.environ['HTTP_MEMBERID'] = memberid  
        
        @app.route('/google-login')
        def authCallback():
            print('auth redirect')
            verifyLogin()
            getOrCreateMember()   
            return jsonify({ 'success': True })

        @app.route('/logout')
        def logout():
            session.pop('state', default=None)
            session.pop('memberid', default=None)
            return jsonify({ 'success': True })

        #app.register_error_handler(Exception, handle_error)

        api.add_resource(CommonApi, '/api/')
        api.add_resource(MemberApi, '/api/members', '/api/members/<id>')
        api.add_resource(GenreApi, '/api/genres', '/api/genres/<id>')
        api.add_resource(SessionLiveApi, '/api/session/live')
        api.add_resource(SessionApi, '/api/session', '/api/session/<id>')
        api.add_resource(SessionEndApi, '/api/session/<id>/end')
        api.add_resource(LayerApi, '/api/session/<sessionId>/layers', '/api/session/<sessionId>/layers/<id>')
        api.add_resource(MatchingQueueApi, '/api/queue', '/api/queue/<id>')

        return app