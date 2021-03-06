import uuid
from flask import jsonify, request
from flask_restful import Resource, reqparse
from app.services.MemberService import *

# Define parser and request args
parser = reqparse.RequestParser()

parser.add_argument('fn', type=str, required=False, location='args')
parser.add_argument('ln', type=str, required=False, location='args')
parser.add_argument('email', type=str, required=False, location='args')

class MemberApi(Resource):

    def get(self, id=None):
        if id != None:
            return jsonify(getById(id))
        args = parser.parse_args()
        firstname = args['fn']
        if firstname != None:
            return jsonify(getByFirstname(firstname))
        lastname = args['ln']
        if lastname != None:
            return jsonify(getByLastname(lastname))
        email = args['email']
        if email != None:
            return jsonify(getByEmail(email))
        return jsonify(getAll())

class MemberOnlineApi(Resource):

    def get(self):
        memberId = request.headers['MEMBERID']
        if memberId == None:
            raise BadRequestException('no member id')
        memberId = uuid.UUID(memberId)
        return jsonify(getAllOnline(memberId))