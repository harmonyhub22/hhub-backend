import uuid
from app.bucket.bucket import deleteBucketFile, uploadBucketFile
from app.db.models.Layer import Layer
from app.db.db import db
from app.services.SessionService import getById as getSessionById
from app.exceptions.BadRequestException import BadRequestException
from app.exceptions.ServerErrorException import ServerErrorException

def getById(id):
    return Layer.query.get(id)

def getAll():
    return Layer.query.all()

def getAllBySessionId(sessionId):
    return Layer.query.filter(Layer.sessionId==sessionId).all()

def uploadFile(sessionId, layerId, memberId, layerFile, fileName, contentType):
    session = getSessionById(sessionId)
    if (session == None or (session.member1Id != memberId and session.member2Id != memberId)):
        raise BadRequestException('you cannot upload this file')
    layer = getById(layerId)
    if layer == None:
        raise BadRequestException('layer with this id does not exist')

    if layer.bucketUrl != None:
        deleteBucketFile(layer.bucketUrl)
    
    url = uploadBucketFile(layerFile, fileName, contentType)

    layer.bucketUrl = url
    db.session.commit()

    return layer

def addOrEditLayer(sessionId, memberId, data, layerId=None):
    session = getSessionById(sessionId)
    if session is None:
        raise BadRequestException('session not found')
    if session.member1Id != memberId and session.member2Id != memberId:
        raise BadRequestException('you are not part of this session') # they aren't part of the session

    name = data['name']
    startTime = data['startTime']
    duration = data['duration']
    fadeInDuration = data['fadeInDuration']
    fadeOutDuration = data['fadeOutDuration']
    trimmedStartDuration = data['trimmedStartDuration']
    trimmedEndDuration = data['trimmedEndDuration']
    fileName = data['fileName']
    y = data['y']
    if layerId == None: # adding a new layer
        try:
            record = Layer(sessionId, memberId, name, startTime, duration, fadeInDuration,
                fadeOutDuration, trimmedStartDuration, trimmedEndDuration, None, fileName, y)
            db.session.add(record)
            db.session.commit()
            return record
        except Exception:
            db.session.rollback()
            raise ServerErrorException('could not add layer')
    try: # editing existing layer
        existing_record = Layer.query.get(layerId)
        existing_record.name = name
        existing_record.startTime = startTime
        existing_record.duration = duration
        existing_record.fadeInDuration = fadeInDuration
        existing_record.fadeOutDuration = fadeOutDuration
        existing_record.reversed = reversed
        existing_record.trimmedStartDuration = trimmedStartDuration
        existing_record.trimmedEndDuration = trimmedEndDuration
        existing_record.fileName = fileName
        existing_record.y = y
        db.session.commit()
        return existing_record
    except:
        db.session.rollback()
        raise ServerErrorException('could not edit layer')

def deleteFile(sessionId, layerId, memberId):
    session = getSessionById(sessionId)
    if (session == None or (session.member1Id != memberId and session.member2Id != memberId)):
        raise BadRequestException('you cannot delete this file')
    layer = getById(layerId)

    if layer is None:
        raise BadRequestException('layer does not exist')
    if layer.bucketUrl == None:
        raise BadRequestException('layer has no url yet')
    
    deleteBucketFile(layer.bucketUrl)
    layer.bucketUrl = None
    db.session.commit()
    return layer

def deleteLayer(sessionId, memberId, layerId):
    session = getSessionById(sessionId)
    if (session == None or (session.member1Id != memberId and session.member2Id != memberId)):
        raise BadRequestException('you cannot delete this layer')

    layerId = uuid.UUID(layerId)
    layer = getById(layerId)
    if layer == None: # already deleted
        return {}
    if layer.sessionId != uuid.UUID(sessionId):
        raise BadRequestException('layer is not in this session')
    
    if layer.bucketUrl != None:
        deleteFile(sessionId, layerId, memberId)

    try:
        db.session.delete(layer)
        db.session.commit()
        return layer
    except Exception:
        db.session.rollback()

'''
def deleteAllFiles():
    layers = getAll()
    deleteAllLayerFiles(layers)
'''