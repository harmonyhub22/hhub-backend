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

def addMember(email, firstname, lastname):
    #db.session.begin()
    try:
        member = Member(email, firstname, lastname, isOnline=True)
        db.session.add(member)
        db.session.commit()
        return member
    except Exception:
        db.session.rollback()
        raise ServerErrorException('could not add member')
    
def editMember(id, data):
    firstname = data['firstname']
    lastname = data['lastname']
    db.session.begin()
    try:
        member = getById(id)
        member.firstname = firstname
        member.lastname = lastname
        member.isOnline = True
        db.session.commit()
        return member
    except Exception:
        db.session.rollback()
        raise ServerErrorException('could not edit member')

def deleteMember(memberId):
    db.session.begin()
    try:
        member = Member.query.get(memberId)
        db.session.delete(member)
        db.session.commit()
        return member
    except Exception:
        db.session.rollback()
        raise ServerErrorException('could not delete member')