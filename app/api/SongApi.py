import uuid
from flask import jsonify, request
from flask_restful import Resource, reqparse
from app.services.SongService import *

# Define parser and request args
parser = reqparse.RequestParser()
parser.add_argument('sessionId', type=str, required=False, location='args')
parser.add_argument('name', type=str, required=False, location='args')
parser.add_argument('memberId',type=str,required=False,location ='args')

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
        memberId = args['memberId']
        if memberId != None:
            memberId = uuid.UUID(memberId)
            return jsonify(getAllByUser(memberId))
        return jsonify(getAll())

    def post(self, sessionId):
        data = request.get_json(force=True)
        memberId = request.headers['MEMBERID']
        
        if not memberId:
            raise BadRequestException('no member ID')
        memberId = uuid.UUID(memberId)
        return jsonify(addSong(sessionId, memberId, data))

    def delete(self, id):
        memberId = request.headers['MEMBERID']
        memberId = uuid.UUID(memberId)
        return jsonify(deleteSong(id, memberId))