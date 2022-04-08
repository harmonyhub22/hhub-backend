from http import HTTPStatus
import uuid
from flask import Response, jsonify, request
from flask_restful import Resource, reqparse
from app.exceptions.BadRequestException import BadRequestException
from app.services.MatchingQueueService import leave, getAll, getById, getByMemberId, joinOrAttemptMatch

# Define parser and request args
parser = reqparse.RequestParser()
parser.add_argument('memberId', type=str, required=False, location='args')

class MatchingQueueApi(Resource):

    def get(self, id=None):
        if id != None:
            return jsonify(getById(id))
        args = parser.parse_args()
        memberId = args['memberId']
        if memberId != None:
            memberId = uuid.UUID(memberId)
            return jsonify(getByMemberId(memberId))
        return jsonify(getAll())

    def post(self):
        memberId = request.headers['MEMBERID']
        return jsonify(joinOrAttemptMatch(memberId))

    def delete(self):
        memberId = request.headers['MEMBERID']
        if memberId == None:
            raise BadRequestException('no member id found')
        memberId = uuid.UUID(memberId)
        leave(memberId)
        return Response(status=HTTPStatus.NO_CONTENT)

