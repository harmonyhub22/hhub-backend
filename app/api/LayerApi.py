from flask import jsonify
from flask_restful import Resource, reqparse
from app.db.models.Genre import Genre

# Define parser and request args
parser = reqparse.RequestParser()

# From http cookies
# parser.add_argument('hhubToken', type=str, required=False, location='cookies')

class LayerApi(Resource):

    def get(self, id=None):
        if id != None:
            return jsonify(Genre.query.get(id))
        return jsonify(Genre.query.all())