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
        memberId = request.headers['MEMBERID']
        if not memberId:
            raise BadRequestException('no member ID')

        # get all sessions with the given member ID
        memberSessions = getAllByMemberId(memberId)
        if not memberSessions:
            raise BadRequestException('member has not joined any sessions')
        if id == None:
            return jsonify(memberSessions)

        # get the session with the given member ID and session ID
        else:
            for s in memberSessions:
                if s.sessionId == uuid.UUID(id):
                    return jsonify(s)
            raise BadRequestException('no session exists with this session ID and member ID')

class SessionEndApi(Resource):
    def post(self, id):
        memberId = request.headers['MEMBERID']
        return jsonify(endSession(memberId, id))

class SessionLiveApi(Resource):
    def get(self):
        memberId = request.headers['MEMBERID']
        return jsonify(getLiveSession(memberId))