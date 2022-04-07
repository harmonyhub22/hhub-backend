import uuid
from flask import jsonify, request
from flask_restful import Resource, reqparse
from app.services.SessionService import *
from app.exceptions.BadRequestException import BadRequestException

# Define parser and request args
parser = reqparse.RequestParser()
parser.add_argument('memberId', type=str, required=False, location='args')

class SessionApi(Resource):

    def get(self, id=None):
        if id == None:
            return jsonify(getAll())
        else:   
            # TODO: refactor this
            memberId = request.headers['MEMBERID']
            memberSessions = getAllByMemberId(memberId)
            if id != None:
                for i in memberSessions:
                    print(i.sessionId)
                    if i.sessionId == uuid.UUID(id):
                        return jsonify(i)
                raise BadRequestException('no session with this id')
            args = parser.parse_args()
            member2Id = args['memberId']
            if member2Id != None:
                member2Id = uuid.UUID(member2Id)
                for i in memberSessions:
                    if i.member1Id == member2Id or i.member2Id == member2Id:
                        return jsonify(i)
                raise BadRequestException('no session with this member')
            return jsonify(memberSessions)

class SessionEndApi(Resource):
    def post(self, id):
        memberId = request.headers['MEMBERID']
        return jsonify(endSession(memberId, id))

class SessionLiveApi(Resource):
    def get(self):
        memberId = request.headers['MEMBERID']
        return jsonify(getLiveSession(memberId))