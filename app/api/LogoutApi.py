import os
from flask import jsonify, make_response
from flask_restful import Resource

class LogoutApi(Resource):

    def post(self):
        resp = make_response(jsonify({}), 200)
        resp.delete_cookie('hhub-token', path="/", domain=os.getenv('COOKIE_DOMAIN'))
        return resp