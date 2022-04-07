import uuid
from flask import jsonify, request
from app.exceptions.BadRequestException import BadRequestException
from werkzeug.utils import secure_filename
from app.services.LayerService import deleteFile, uploadFile
from app.services.SongService import uploadSong
from flask import Blueprint

layerUploadBlueprint = Blueprint('layer_upload_blueprint', __name__, url_prefix='/api/session/<sessionId>/layers/<layerId>')
songUploadBlueprint = Blueprint('song_upload_blueprint', __name__, url_prefix='/api/session/<sessionId>')

@layerUploadBlueprint.route('/upload', methods=['POST', 'PUT'])
def postLayer(sessionId, layerId):
    memberId = request.headers['MEMBERID']
    memberId = uuid.UUID(memberId)

    layerFile = request.files['file']
    if not layerFile:
        raise BadRequestException('file not provided')

    fileName = secure_filename(layerFile.filename)
    contentType = request.mimetype

    return jsonify(uploadFile(sessionId, layerId, memberId, layerFile, fileName, contentType))

@layerUploadBlueprint.route('/delete', methods=['DELETE'])
def deleteLayer(sessionId, layerId):
    memberId = request.headers['MEMBERID']
    memberId = uuid.UUID(memberId)

    return jsonify(deleteFile(sessionId, layerId, memberId))

@songUploadBlueprint.route('/upload', methods=['PUT'])
def putSong(sessionId):

    songFile = request.files['file']
    if not songFile:
        raise BadRequestException('file not provided')

    fileName = secure_filename(songFile.filename)
    contentType = request.mimetype

    return jsonify(uploadSong(sessionId, songFile, fileName, contentType))