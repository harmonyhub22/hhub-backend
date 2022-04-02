from flask import jsonify
from flask_restful import Resource, reqparse
from app.services.GenreService import *

# Define parser and request args
parser = reqparse.RequestParser()

parser.add_argument('name', type=str, required=False, location='args')

class GenreApi(Resource):

    def get(self, id=None):
        if id != None:
            return jsonify(getById(id))
        args = parser.parse_args()
        name = args['name']
        if name != None:
            return jsonify(getByName(name))
        return jsonify(getAll())