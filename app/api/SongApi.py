import uuid
from flask import jsonify, request
from flask_restful import Resource, reqparse
from app.services.SongService import *

# Define parser and request args
parser = reqparse.RequestParser()
parser.add_argument('sessionId', type=str, required=False, location='args')
parser.add_argument('name', type=str, required=False, location='args')

class SongApi(Resource):

    def get(self, id=None):
        if id != None:
            return jsonify(getById(id))
        args = parser.parse_args()
        sessionId = args['sessionId']
        if sessionId != None:
            sessionId = uuid.UUID(sessionId)
            return jsonify(getBySessionId(sessionId))
        name = args['name']
        if name != None:
            return jsonify(getByName(name))
        return jsonify(getAll())

    def delete(self, id):
        memberId = request.headers['MEMBERID']
        memberId = uuid.UUID(memberId)
        return jsonify(deleteSong(id, memberId))