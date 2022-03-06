import uuid
from app.db.models.Layer import Layer
from app.db.db import db
from app.services.SessionService import getById as getSessionById
from app.services.MemberService import getById as getMemberById
from app.exceptions.BadRequestException import BadRequestException
from app.exceptions.ServerErrorException import ServerErrorException
import os
import google.cloud.storage as storage
CLOUD_STORAGE_BUCKET = os.environ['CLOUD_STORAGE_BUCKET']
def getById(id):
    return Layer.query.get(id)

def getAllBySessionId(sessionId):
    return Layer.query.filter(Layer.sessionId==sessionId).all()

def uploadLayerFile(sessionId,layerId,fileData):
    destinationFileName = "{}-{}".format(sessionId,layerId)
    if not fileData:
        return 'No file uploaded.', 400
    gcs=storage.Client.from_service_account_json('D:\hhub-backend\keys.json')

    # Get the bucket that the file will be uploaded to.
    bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)
    blob = bucket.blob(destinationFileName)
    blob.upload_from_filename(fileData)
    blob.make_public()
    Layer.bucketUrl = blob.public_url
    return blob.public_url


def addOrEditLayer(sessionId, memberId, data, layerId=None):

    session = getSessionById(sessionId)
    if session.member1Id != memberId and session.member2Id != memberId:
        raise BadRequestException('you are not part of this session') # they aren't part of the session

    startTime = data['startTime']
    endTime = data['endTime']
    repeatCount = data['repeatCount']
    bucketUrl = data['bucketUrl']
    if layerId == None: # adding a new layer
        # TODO: Genereate bucket url
        try:
            record = Layer(sessionId, startTime, endTime, repeatCount, bucketUrl)
            db.session.add(record)
            db.session.commit()
            return record
        except Exception:
            db.session.rollback()
            raise ServerErrorException('could not add layer')
    try: # editing existing layer
        existing_record = Layer.query.get(layerId)
        existing_record.startTime = startTime

        existing_record.repeatCount = repeatCount
        db.session.commit()
        return existing_record
    except:
        db.session.rollback()
        raise ServerErrorException('could not edit layer')

def deleteLayer(sessionId, memberId, layerId):
    session = getSessionById(sessionId)
    if (session == None or (session.member1Id != memberId and session.member2Id != memberId)):
        raise BadRequestException('you cannot delete this layer')

    layer = getById(layerId)
    if layer == None or layer.sessionId != uuid.UUID(sessionId):
        raise BadRequestException('layer is not in this session')

    try:
        db.session.delete(layer)
        db.session.commit()
        return layer
    except Exception:
        db.session.rollback()
        
