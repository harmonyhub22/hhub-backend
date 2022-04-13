import uuid
from app.db.models.MatchingQueue import MatchingQueue
from app.db.db import db
from app.exceptions.BadRequestException import BadRequestException
from app.exceptions.ServerErrorException import ServerErrorException
from app.services.MemberService import getSid
from app.services.SessionService import createSession, getLiveSession
from app.socket.init import addToRoom, emitMessageToRoom, emitToSid, getSidRooms

def getById(id):
    return MatchingQueue.query.get(id)

def getByMemberId(memberId):
    return MatchingQueue.query.filter(MatchingQueue.memberId==memberId).first()

def getAll():
    return MatchingQueue.query.order_by(MatchingQueue.timeEntered.asc()).all()

def getTop():
    return MatchingQueue.query.order_by(MatchingQueue.timeEntered.asc()).first()

def match(member1Id, queueItem): # if there are 2 users in the queue, create the session with them
    print('queue item memberId', queueItem.memberId)
    newSession = createSession(member1Id, queueItem.memberId)
    print(newSession.sessionId)
    print("session created", newSession.member1.firstname, newSession.member2.lastname)
    db.session.delete(queueItem)
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
    topQueued = getTop()
    if topQueued != None:
        print("top user in queue is", topQueued.member.firstname)
        print("member ID is", memberId)
        print("matching...")
        try:
            session = match(memberId, topQueued)
            print("new session", session.sessionId)
            sid1 = getSid(session.member1.memberId)
            addToRoom(sid1, str('session-' + str(session.sessionId)))
            print('sid1', sid1)
            sid2 = getSid(session.member2.memberId)
            addToRoom(sid2, str('session-' + str(session.sessionId)))
            print('sid2', sid2)
            emitMessageToRoom("session_made", { 'sessionId': str(session.sessionId) }, roomName=str("session-" + str(session.sessionId)))
            return None
        except Exception as e:
            print('exception encountered')
            print(str(e))
            db.session.rollback()
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
    if existing_record == None:
        raise BadRequestException('not in the queue')
    try:
        db.session.delete(existing_record)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise ServerErrorException('could not remove you from the queue')