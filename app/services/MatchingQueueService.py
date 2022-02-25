from app.db.models.MatchingQueue import MatchingQueue
from app.db.db import db
from app.exceptions.BadRequestException import BadRequestException
from app.exceptions.ServerErrorException import ServerErrorException

def getById(id):
    return MatchingQueue.query.get(id)

def getByMemberId(memberId):
    return MatchingQueue.query.filter(MatchingQueue.memberId==memberId).first()

def getAll():
    return MatchingQueue.query.order_by(MatchingQueue.timeEntered.asc()).all()

def join(memberId):
    db.session.begin()
    existing_record = getByMemberId(memberId)
    if existing_record != None:
        return existing_record
    try:
        record = MatchingQueue(memberId)
        db.session.add(record)
        db.session.commit()
        return record
    except Exception:
        db.session.rollback()
        raise ServerErrorException('could not add you to the queue')

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
    # raise BadRequestException('you are not in the queue')