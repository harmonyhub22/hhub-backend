import uuid
from app.db.models.MatchingQueue import MatchingQueue
from app.db.db import db
from app.exceptions.BadRequestException import BadRequestException
from app.exceptions.ServerErrorException import ServerErrorException
from app.services.MemberService import getSid
from app.services.SessionService import createSession, getLiveSession
from app.socket.init import addToRoom, emitMessageToRoom

def getById(id):
    return MatchingQueue.query.get(id)

def getByMemberId(memberId):
    return MatchingQueue.query.filter(MatchingQueue.memberId==memberId).first()

def getAll():
    return MatchingQueue.query.order_by(MatchingQueue.timeEntered.asc()).all()

def getTop():
    return MatchingQueue.query.order_by(MatchingQueue.timeEntered.asc()).first()

def getTop2():
    return MatchingQueue.query.order_by(MatchingQueue.timeEntered.asc()).limit(2).all()

def match(member1Id): # if there are 2 users in the queue, create the session with them
    queueItem = getTop()
    db.session.delete(queueItem)
    db.session.commit()
    newSession = createSession(member1Id, queueItem.memberId)
    db.session.add(newSession)
    db.session.commit()
    return newSession

def joinOrAttemptMatch(memberId):
    liveSession = getLiveSession(memberId)
    if liveSession != None:
        raise BadRequestException('you are currently in a session')
    
    # if user is already in the queue, return existing record
    existing_record = getByMemberId(memberId)
    if existing_record != None:
        return existing_record

    # if theres 1 person currently in the queue, match with them
    if len(getTop2()) == 1:
        session = match(memberId)
        # TODO: uncomment lines 45-49 this after running unit tests
        # sid1 = getSid(session.member1.memberId)
        # sid2 = getSid(session.member2.memberId)
        # addToRoom(sid1, 'session-'+str(session.sessionId))
        # addToRoom(sid2, 'session-'+str(session.sessionId))
        # emitMessageToRoom('session_made', { 'sessionId': session.sessionId }, roomName='session-'+str(session.sessionId))
        return None
    
    # otherwise, get added to the queue
    else:
        try:
            record = MatchingQueue(memberId)
            db.session.add(record)
            db.session.commit()
            return record
        except Exception:
            db.session.rollback()
            raise ServerErrorException('could not add you to the queue')
        
def leave(memberId):
    existing_record = getByMemberId(memberId)
    if existing_record != None:
        try:
            db.session.delete(existing_record)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise ServerErrorException('could not remove you from the queue')