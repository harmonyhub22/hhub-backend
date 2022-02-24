

import os
from dotenv import load_dotenv
from flask import Flask
import sqlalchemy
from app.controllers.member_controller import member_controller_bp
from app.db.db import db
from app.db.seed.data import seed


def create_app(config_file):
    """
    Creating and returning the app
    """

    app_path = os.path.dirname(os.path.abspath(__file__))
    project_folder = os.path.expanduser(app_path)
    load_dotenv(os.path.join(project_folder, '.env'))

    app = Flask(__name__)

    app.config.from_pyfile(config_file)

    db.init_app(app)

    with app.app_context():

        #db.drop_all()

        cmd = "CREATE SCHEMA IF NOT EXISTS " + os.getenv('SCHEMA', 'hhub') + ";"
        db.session.execute(cmd)
        cmd = "SET search_path TO " + os.getenv('SCHEMA', 'hhub') + ";"
        db.session.execute(cmd)
        db.session.commit()
        
        db.create_all()

        seed()

        app.register_blueprint(member_controller_bp, url_prefix='/members')

        return app