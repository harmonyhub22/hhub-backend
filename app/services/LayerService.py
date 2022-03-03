import uuid
from app.db.models.Layer import Layer
from app.db.db import db
from app.services.SessionService import getById as getSessionById
from app.services.MemberService import getById as getMemberById
from app.exceptions.BadRequestException import BadRequestException
from app.exceptions.ServerErrorException import ServerErrorException

def getById(id):
    return Layer.query.get(id)

def getAllBySessionId(sessionId):
    return Layer.query.filter(Layer.sessionId==sessionId).all()

def addOrEditLayer(sessionId, memberId, data, layerId=None):

    session = getSessionById(sessionId)
    if session.member1Id != memberId and session.member2Id != memberId:
        raise BadRequestException('you are not part of this session') # they aren't part of the session

    startMeasure = data['startMeasure']
    repeatCount = data['repeatCount']
    bucketUrl = data['bucketUrl']
    if layerId == None: # adding a new layer
        # TODO: Genereate bucket url
        try:
            record = Layer(sessionId, startMeasure, repeatCount, bucketUrl)
            db.session.add(record)
            db.session.commit()
            return record
        except Exception:
            db.session.rollback()
            raise ServerErrorException('could not add layer')
    try: # editing existing layer
        existing_record = Layer.query.get(layerId)
        existing_record.startMeasure = startMeasure
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
        
