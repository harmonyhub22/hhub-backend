from flask import jsonify
from flask_restful import Resource, reqparse
from app.db.models.Member import Member

# Define parser and request args
parser = reqparse.RequestParser()

# From http cookies
# parser.add_argument('hhubToken', type=str, required=False, location='cookies')
parser.add_argument('fn', type=str, required=False, location='args')
parser.add_argument('ln', type=str, required=False, location='args')
parser.add_argument('email', type=str, required=False, location='args')

class MemberApi(Resource):

    def get(self, id=None):
        if id != None:
            return jsonify(Member.query.get(id))
        args = parser.parse_args()
        firstname = args['fn']
        if firstname != None:
            return jsonify(Member.query.filter_by(firstname=firstname).first())
        lastname = args['ln']
        if firstname != None:
            return jsonify(Member.query.filter_by(lastname=lastname).first())
        email = args['email']
        if email != None:
            return jsonify(Member.query.filter_by(email=email).first())
        return jsonify(Member.query.all())