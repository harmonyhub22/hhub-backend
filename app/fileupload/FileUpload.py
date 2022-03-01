from posixpath import basename
from flask_restful import Resource
from flask_uploads import UploadNotAllowed
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.fileupload import FileHelper
from app.fileupload.Strings import gettext
from app.fileupload.File import FileSchema

file_schema = FileSchema()

class FileUpload(Resource):
    @jwt_required
    def post(self):
        
        data = file_schema.load(request.files)
        user_id = get_jwt_identity()
        folder = f"user_{user_id}"
        try:
            file_path = FileHelper.saveFile(data["files"], folder=folder)
            basename = FileHelper.getBasename(file_path)
            return {"message": gettext("file_uploaded").format(basename) }, 201
            
        except UploadNotAllowed:
            extension = FileHelper.getExtension(data["files"])
            return {"message": gettext("file_illegal_extension").format(extension)}, 400
            