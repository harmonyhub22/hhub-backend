from flask import jsonify
from flask_restful import Resource, reqparse
from app.db.models.Session import Session
from app.services.SessionService import *

# Define parser and request args
parser = reqparse.RequestParser()

parser.add_argument('userId', type=str, required=False, location='args')

class SessionApi(Resource):

    def get(self, id=None):
        if id != None:
            return jsonify(getById(id))
        args = parser.parse_args()
        userId = args['userId']
        if userId != None:
            return jsonify(getByUserId(userId))
        return jsonify(getAll())