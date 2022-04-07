from flask import jsonify, request, session
from flask_restful import Resource, reqparse
from app.services.MemberService import deleteMember, editMember, getById

# Define parser and request args
parser = reqparse.RequestParser()

class CommonApi(Resource):

    def get(self):
        memberId = request.headers['MEMBERID']
        return jsonify(getById(memberId))

    def put(self):
        data = request.get_json(force=True)
        memberId = request.headers['MEMBERID']
        return jsonify(editMember(memberId, data))

    def delete(self):
        memberId = request.headers['MEMBERID']
        session.clear()
        return jsonify(deleteMember(memberId))