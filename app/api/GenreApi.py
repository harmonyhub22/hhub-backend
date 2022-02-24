from flask import jsonify
from flask_restful import Resource, reqparse
from app.db.models.Genre import Genre

# Define parser and request args
parser = reqparse.RequestParser()

# From http cookies
# parser.add_argument('hhubToken', type=str, required=False, location='cookies')
parser.add_argument('name', type=str, required=False, location='args')

class GenreApi(Resource):

    def get(self, id=None):
        if id != None:
            return jsonify(Genre.query.get(id))
        args = parser.parse_args()
        print(args)
        name = args['name']
        if name != None:
            return jsonify(Genre.query.filter_by(name=name).first())
        return jsonify(Genre.query.all())