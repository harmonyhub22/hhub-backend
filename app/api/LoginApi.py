from flask import jsonify, make_response, request, session
from flask_restful import Resource
from app.services.MemberService import deleteMember, addMember, getByEmail, getById

class LoginApi(Resource):

    def post(self):
        data = request.get_json(force=True)
        memberId = None
        try:
            memberId = request.headers['MEMBERID']
            return jsonify(getById(memberId))
        except:
            member = getByEmail(data['email'])
            if member == None:
                member = addMember(memberId, data['email'], data['firstname'], data['lastname'])
            resp = make_response(jsonify(member), 200)
            resp.set_cookie('memberId', value=str(member.memberId))
            return resp