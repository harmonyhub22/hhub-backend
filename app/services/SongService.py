from app.bucket.bucket import deleteBucketFile
from app.db.models.Song import Song
from app.db.models.Session import Session
from sqlalchemy import func
from app.db.db import db
from app.exceptions.BadRequestException import BadRequestException
from app.exceptions.ServerErrorException import ServerErrorException
from app.exceptions.UnauthorizedException import UnauthorizedException
from app.services.SessionService import getById as getSessionById

def getById(id):
    return Song.query.get(id)

def getByName(name):
    return Song.query.filter(func.lower(Song.name)==func.lower(name)).all()

def getBySessionId(sessionId):
    return Song.query.filter(Song.sessionId==sessionId).first()

def getAll():
    return Song.query.all()
    
def getAllByUser(memberId):
    return Session.query.join(Song, Session.sessionId==Song.sessionId).filter((Session.member1Id==memberId) | (Session.member2Id==memberId)).order_by(Song.createdAt).all()

def getAllBySessionId(sessionId):
    return Song.query.filter(Song.sessionId==sessionId).all()

def deleteSong(songId, memberId):
    song = getById(songId)
    if song == None:
        print('no song found')
        raise ServerErrorException('no song found')
    if song.session.member1.memberId != memberId and song.session.member2.memberId != memberId:
        raise UnauthorizedException('you cannot delete this song')
    songs = getAllBySessionId(song.sessionId)
    if songs != None and len(songs) == 1:
        try:
            if song.session.bucketUrl != None:
                deleteBucketFile(song.session.bucketUrl)
        except Exception:
            raise ServerErrorException('could not delete song')
    try: 
        db.session.delete(song)
        db.session.commit()
        return song
    except Exception:
        db.session.rollback()
        raise ServerErrorException('could not delete song')