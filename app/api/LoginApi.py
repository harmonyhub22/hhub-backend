from flask import jsonify, make_response, request, session
from flask_restful import Resource
from app.services.MemberService import deleteMember, addMember, getByEmail, getById

class LoginApi(Resource):

    def post(self):
        data = request.get_json(force=True)
        print("Json data: ", data)
        memberId = None
        try:
            memberId = request.headers['MEMBERID']
            print('memberId', memberId)
            return jsonify(getById(memberId))
        except:
            print('logging in')
            member = getByEmail(data['email'])
            if member == None:
                member = addMember(data['email'], data['firstname'], data['lastname'])
            print('memberId', member.memberId)
            resp = make_response(jsonify(member), 200)
            resp.set_cookie('memberId', value=str(member.memberId))
            return resp