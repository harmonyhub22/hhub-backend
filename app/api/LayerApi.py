import uuid
from flask import jsonify, request
from flask_restful import Resource, reqparse
from app.services.LayerService import *

# Define parser and request args
parser = reqparse.RequestParser()

class LayerApi(Resource):

    def get(self, sessionId, id=None):
        if id != None:
            return jsonify(getById(id))
        return jsonify(getAllBySessionId(sessionId))

    def post(self, sessionId, id=None):
        data = request.get_json(force=True)
        memberId = request.headers['MEMBERID']
        memberId = uuid.UUID(memberId)
        return jsonify(addOrEditLayer(sessionId, memberId, data, id))

    def delete(self, sessionId, id):
        memberId = request.headers['MEMBERID']
        memberId = uuid.UUID(memberId)
        return jsonify(deleteLayer(sessionId, memberId, id))