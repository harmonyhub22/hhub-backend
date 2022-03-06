from distutils.command.upload import upload
import uuid
from flask import jsonify, request
from flask_restful import Resource, reqparse
from werkzeug.datastructures import FileStorage
from app.services.LayerService import *

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
    #upload file to bucket, get object url, update bucket url record, return layer
    def put(self,sessionId,id):
        fileData = request.files['file']
        # call service to upload to bucket
        # call service to set layer.bucketUrl = 
        return jsonify(uploadLayerFile(sessionId,id,fileData))
    def delete(self, sessionId, id):
        memberId = request.headers['MEMBERID']
        memberId = uuid.UUID(memberId)
        return jsonify(deleteLayer(sessionId, memberId, id))