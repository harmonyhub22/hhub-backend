import datetime
import uuid
from app.bucket.bucket import deleteBucketFile
from app.db.models.Session import Session
from app.db.db import db
from app.services.MemberService import updateSid
from app.services.MemberService import getById as getMemberById
from app.exceptions.BadRequestException import BadRequestException
from app.exceptions.ServerErrorException import ServerErrorException

def getById(id):
    return Session.query.get(id)

def getByMemberId(memberId):
    return Session.query.filter((Session.member1Id==memberId) | (Session.member2Id==memberId)).first()

def getAllByMemberId(memberId):
    return Session.query.filter((Session.member1Id==memberId) | (Session.member2Id==memberId)).all()

def getAll():
    return Session.query.all()

def getLiveSession(memberId):
    return Session.query.filter(((Session.member1Id==memberId) | (Session.member2Id==memberId)) & (Session.endTime==None)).first()

def createSession(member1Id, member2Id):
    member1 = getMemberById(member1Id)
    member2 = getMemberById(member2Id)
    print(member1.firstname, member2.firstname)
    if member2 == None or member1 == None:
        print('a member does not exist')
        raise BadRequestException('member does not exist')
    print('members exists')
    if member2Id == member1Id:
        raise BadRequestException('cannot start session with yourself')
    print('they are not the same')
    existing_session = Session.query.filter(((Session.member1Id==member1Id) | (Session.member2Id==member2Id)
                                         | (Session.member1Id==member2Id) | (Session.member2Id==member1Id))
                                         & (Session.endTime==None)).first()
    if existing_session != None:
        print('theres an existing session')
        raise BadRequestException('you or other member is already in a Session')
    print("no existing session")

    record = Session(member1Id, member2Id)
    print('created record')
    db.session.add(record)
    print('added record')
    db.session.commit()
    print('committed record')
    return record

def endSession(memberId, sessionId):
    session = Session.query.get(sessionId)
    memberId = uuid.UUID(memberId)
    if session == None or (session.member1Id != memberId and session.member2Id != memberId):
        raise BadRequestException('you cannot modify this Session')
    for layer in session.layers:
        if layer.bucketUrl != None:
            try:
                deleteBucketFile(layer.bucketUrl)
            except Exception:
                pass
        try:
            db.session.delete(layer)
            db.session.commit()
        except Exception:
            pass
    try:
        updateSid(memberId, None)
    except Exception:
        pass
    try:
        session.endTime = datetime.datetime.utcnow()
        db.session.commit()
        return session
    except Exception:
        db.session.rollback()
        raise ServerErrorException('cannot end Session')