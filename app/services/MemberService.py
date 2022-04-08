from app.db.models.Member import Member
from app.db.db import db
from sqlalchemy import func
from app.exceptions.BadRequestException import BadRequestException
from app.exceptions.ServerErrorException import ServerErrorException

def getById(id):
    return Member.query.get(id)

def getByFirstname(fn):
    return Member.query.filter(func.lower(Member.firstname)==func.lower(fn)).first()

def getByLastname(ln):
    return Member.query.filter(func.lower(Member.lastname)==func.lower(ln)).first()

def getByEmail(email):
    return Member.query.filter(func.lower(Member.email)==func.lower(email)).first()

def getAll():
    return Member.query.all()

def getBySid(sid):
    return Member.query.filter(Member.sid==sid).first()

def getAllOnline(memberId):
    return Member.query.filter((Member.isOnline==True) & (Member.memberId!=memberId)).all()

def addMember(email, firstname, lastname):
    try:
        member = Member(email, firstname, lastname, isOnline=True)
        db.session.add(member)
        db.session.commit()
        return member
    except Exception:
        db.session.rollback()
        raise ServerErrorException('could not add member')
    
def editMember(id, data):
    email = data['email']
    firstname = data['firstname']
    lastname = data['lastname']
    try:
        member = getById(id)
        if email != None:
            member.email = email
        if firstname != None:
            member.firstname = firstname
        if lastname != None:
            member.lastname = lastname
        db.session.commit()
        return member
    except Exception:
        db.session.rollback()
        raise ServerErrorException('could not edit member')

def deleteMember(memberId):
    try:
        member = getById(memberId)
        db.session.delete(member)
        db.session.commit()
        return member
    except Exception:
        db.session.rollback()
        raise ServerErrorException('could not delete member')

def setOnline(memberId):
    member = getById(memberId)
    member.isOnline = True
    db.session.commit()

def setOffline(memberId):
    member = getById(memberId)
    member.isOnline = False
    db.session.commit()

# web socket utils
def getSid(memberId):
    return getById(memberId).sid

def setSid(memberId, sid):
    try:
        member = getById(memberId)
        member.sid = sid
        member.isOnline = True
        db.session.commit()
        return member.sid
    except Exception:
        db.session.rollback()
        raise ServerErrorException('could not add sid to member')

def updateSid(memberId, sid=None):
    try:
        member = getById(memberId)
        member.sid = sid
        if sid == None:
            member.isOnline = False
        db.session.commit()
        return member.sid
    except Exception:
        db.session.rollback()
        raise ServerErrorException('could not add sid to member')