import uuid
from flask import jsonify
from flask_restful import Resource, reqparse
#from app.services.MatchinQueueService import *

# Define parser and request args
parser = reqparse.RequestParser()
parser.add_argument('userId', type=uuid, required=False, location='args')

class LayerApi(Resource):

    '''
    def get(self, id=None):
        if id != None:
            return jsonify(getById(id))
        return jsonify(getAllBySessionId(sessionId))
    '''