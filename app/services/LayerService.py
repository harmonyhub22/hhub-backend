import uuid
from app.bucket.bucket import deleteBucketFile, uploadBucketFile
from app.db.models.Layer import Layer
from app.db.db import db
from app.services.SessionService import getById as getSessionById
from app.exceptions.BadRequestException import BadRequestException
from app.exceptions.ServerErrorException import ServerErrorException

def getById(id):
    return Layer.query.get(id)

def getAllBySessionId(sessionId):
    return Layer.query.filter(Layer.sessionId==sessionId).all()

def uploadFile(sessionId, layerId, memberId, file, filename, contentType):
    session = getSessionById(sessionId)
    if (session == None or (session.member1Id != memberId and session.member2Id != memberId)):
        raise BadRequestException('you cannot edit this layer')
    layer = getById(layerId)
    if layer == None:
        raise BadRequestException('layer with this id does not exist')

    if layer.bucketUrl != None:
        deleteBucketFile(layer.bucketUrl)
    
    url = uploadBucketFile(file, filename, contentType)

    layer.bucketUrl = url
    db.session.commit()

    return layer

def addOrEditLayer(sessionId, memberId, data, layerId=None):
    session = getSessionById(sessionId)
    if session.member1Id != memberId and session.member2Id != memberId:
        raise BadRequestException('you are not part of this session') # they aren't part of the session

    startTime = data['startTime']
    endTime = data['endTime']
    repeatCount = data['repeatCount']
    if layerId == None: # adding a new layer
        # TODO: Genereate bucket url
        try:
            record = Layer(sessionId, startTime, endTime, repeatCount, '')
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

def deleteFile(sessionId, layerId, memberId):
    session = getSessionById(sessionId)
    if (session == None or (session.member1Id != memberId and session.member2Id != memberId)):
        raise BadRequestException('you cannot edit this layer')
    layer = getById(layerId)

    if layer.bucketUrl == None:
        return layer
    
    deleteBucketFile(layer.bucketUrl)
    layer.bucketUrl = None
    db.session.commit()
    return layer
