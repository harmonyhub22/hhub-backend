from app.bucket.bucket import deleteBucketFile, uploadBucketFile
from app.db.models.Song import Song
from app.db.models.Session import Session
from sqlalchemy import func
from app.db.db import db
from app.exceptions.BadRequestException import BadRequestException
from app.exceptions.ServerErrorException import ServerErrorException
from app.exceptions.UnauthorizedException import UnauthorizedException
from app.services.SessionService import getById as getSessionById
from app.bucket.bucket import deleteAllSongFiles

def getById(id):
    return Song.query.get(id)

def getByName(name):
    return Song.query.filter(func.lower(Song.name)==func.lower(name)).all()

def getBySessionId(sessionId):
    return Song.query.filter(Song.sessionId==sessionId).first()

def getAll():
    return Song.query.all()
    
def getAllByUser(memberId):
    return Song.query.join(Session, Session.sessionId==Song.sessionId).filter(Song.memberId==memberId).order_by(Song.createdAt).all()

def getAllBySessionId(sessionId):
    return Song.query.filter(Song.sessionId==sessionId).all()

def deleteSong(songId, memberId):
    song = getById(songId)
    if song == None:
        raise ServerErrorException('no song found')
    if song.session.member1.memberId != memberId and song.session.member2.memberId != memberId:
        raise UnauthorizedException('you cannot delete this song')
    songs = getAllBySessionId(song.sessionId)
    if songs != None and len(songs) == 1:
        try:
            if song.session.bucketUrl != None:
                deleteBucketFile(song.session.bucketUrl)
                print('deleted bucket file')
                song.session.bucketUrl = None
                db.session.commit()
        except Exception:
            raise ServerErrorException('could not delete song')
    try:
        print('deleting song by', song.session.member1.firstname, 'and', song.session.member2.firstname)
        db.session.delete(song)
        db.session.commit()
        return song
    except Exception:
        db.session.rollback()
        raise ServerErrorException('could not delete song')

def addSong(sessionId, memberId, data):
    name = data.get('name')
    if name == None:
        raise BadRequestException('song name not provided')
    
    session = getSessionById(sessionId)
    if session == None:
        raise BadRequestException('session does not exist')
    
    if session.member1.memberId != memberId and session.member2.memberId != memberId:
        raise UnauthorizedException('unable to save this song')

    try:
        song = Song(sessionId, memberId, name)   
        db.session.add(song)
        db.session.commit()
        return song
    except Exception:
        db.session.rollback()
        raise ServerErrorException('could not add song')

def uploadSong(sessionId, memberId, songFile, fileName, contentType):
    session = getSessionById(sessionId)
    if (session == None or (session.member1Id != memberId and session.member2Id != memberId)):
        raise BadRequestException('you cannot upload this file')
    if session.bucketUrl != None:
        return session
    
    url = uploadBucketFile(songFile, fileName, contentType)

    session.bucketUrl = url
    db.session.commit()
    return session