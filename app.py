from flask import Flask, request
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from grpc import method_handlers_generic_handler
from sympy import re
from flask_socketio import *

import os

app = Flask(__name__)

app.config.from_object(os.getenv('APP_SETTINGS', 'config.DevelopmentConfig'))
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
print(os.getenv('DATABASE_URL'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# must import the models to it creates them
from models.User import User
from models.UserFriend import UserFriend
from models.UserFriendRequest import UserFriendRequest
from models.Genre import Genre
from models.Session import Session
from models.Layer import Layer

db.create_all()

migrate = Migrate(app, db)

@app.route("/")
def hello_world():
    return "Welcome to the Harmony Hub Server"

@app.route("/ping", methods=['GET'])
def ping():
    return jsonify(success=True)

import seed
seed()

    
