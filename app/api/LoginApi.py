from flask import jsonify, make_response, request, session
from flask_restful import Resource, reqparse
from app.services.MemberService import deleteMember, addMember, getByEmail, getById

# Define parser and request args
parser = reqparse.RequestParser()

class LoginApi(Resource):

    def post(self):
        data = request.get_json(force=True)
        memberId = None
        try:
            memberId = request.headers['MEMBERID']
            print('memberId', memberId)
            return jsonify({})
        except:
            print('logging in')
            member = getByEmail(data['email'])
            if member == None:
                member = addMember(memberId, data['email'], data['firstname'], data['lastname'])
            print('memberId', member.memberId)
            resp = make_response(jsonify({}), 200)
            resp.set_cookie('memberId', value=str(member.memberId))
            return resp