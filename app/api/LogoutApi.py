from flask import jsonify, make_response
from flask_restful import Resource

class LogoutApi(Resource):

    def post(self):
        resp = make_response(jsonify({}), 200)
        resp.delete_cookie('memberId')
        return resp