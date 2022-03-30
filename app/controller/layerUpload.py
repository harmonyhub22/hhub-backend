import uuid
from flask import jsonify, request
from app.exceptions.BadRequestException import BadRequestException
from werkzeug.utils import secure_filename
from app.services.LayerService import deleteFile, uploadFile
from flask import Blueprint

layerUploadBlueprint = Blueprint('layer_upload_blueprint', __name__, url_prefix='/api/session/<sessionId>/layers/<layerId>')

@layerUploadBlueprint.route('/upload', methods=['POST', 'PUT'])
def layerPost(sessionId, layerId):

    memberId = request.headers['MEMBERID']
    memberId = uuid.UUID(memberId)

    file = request.files['file']
    if not file:
        raise BadRequestException('file not provided')

    filename = secure_filename(file.filename)
    contentType = request.mimetype

    return jsonify(uploadFile(sessionId, layerId, memberId, file, filename, contentType))

@layerUploadBlueprint.route('/delete', methods=['DELETE'])
def layerDelete(sessionId, layerId):

    memberId = request.headers['MEMBERID']
    memberId = uuid.UUID(memberId)

    return jsonify(deleteFile(sessionId, layerId, memberId))