from flask import jsonify, request
from flask_restful import Resource, reqparse
from app.services.MemberService import getById as getMemberById

# Define parser and request args
parser = reqparse.RequestParser()

class CommonApi(Resource):

    def get(self):
        memberId = request.headers['MEMBERID']
        print('common')
        return jsonify(getMemberById(memberId))