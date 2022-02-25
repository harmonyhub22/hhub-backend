from flask import jsonify
from flask_restful import Resource, reqparse
from app.services.LayerService import *

# Define parser and request args
parser = reqparse.RequestParser()

class LayerApi(Resource):

    def get(self, sessionId, id=None):
        if id != None:
            return jsonify(getById(id))
        return jsonify(getAllBySessionId(sessionId))