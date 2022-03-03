import uuid
from app.db.models.MatchingQueue import MatchingQueue
from app.db.db import db
from app.exceptions.BadRequestException import BadRequestException
from app.exceptions.ServerErrorException import ServerErrorException
from app.services.SessionService import createSession
from app.socket.utils import addToRoom, emitMessageToRoom, getSids

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
    newSession = createSession(member1Id, queueItem.memberId, uuid.UUID('dff3c144-eb29-41d3-82ea-9bcd200fc891')) # default genre
    return newSession

def joinOrAttemptMatch(memberId):
    db.session.begin()
    existing_record = getByMemberId(memberId)
    if existing_record != None:
        return existing_record
    if len(getTop2()) < 2:
        try:
            record = MatchingQueue(memberId)
            db.session.add(record)
            db.session.commit()
            return record
        except Exception:
            db.session.rollback()
            raise ServerErrorException('could not add you to the queue')
    else:
        session = match(memberId)
        sid1, sid2 = getSids(session.member1.memberId, session.member2.memberId)
        addToRoom(sid1, 'session='+str(session.sessionId))
        addToRoom(sid2, 'session='+str(session.sessionId))
        emitMessageToRoom('session_made', { 'sessionId': session.sessionId }, roomName='session='+str(session.sessionId))
        return None


def leave(memberId):
    db.session.begin()
    existing_record = getByMemberId(memberId)
    if existing_record != None:
        try:
            db.session.delete(existing_record)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise ServerErrorException('could not remove you from the queue')