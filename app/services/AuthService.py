import datetime
from msilib.schema import Error
import os
from app.db.models.Auth import Auth
from sqlalchemy import func
from app.db.db import db
from app.exceptions.ServerErrorException import ServerErrorException
from app.exceptions.UnauthorizedException import UnauthorizedException
import jwt

def generateToken(memberId):
    secret = os.environ.get("SECRET_KEY", None)
    if secret == None:
        raise Exception
        return
    
    token = jwt.encode({
        'memberId': str(memberId),
        'exp' : datetime.utcnow() + datetime.timedelta(hours=24)
    }, secret)

    return token

def getByMemberId(memberId):
    return Auth.query.filter(Auth.memberId == memberId).first()

def addOrUpdateAuth(memberId, password):
    try:
        # query for a member first, 
        auth = getByMemberId(memberId)
        if auth == None:
            newAuth = Auth(memberId, password)
            db.session.add(newAuth)
            db.session.commit()
        else:
            auth.password = password
            db.session.commit()

    except Exception:
        db.session.rollback()
        raise ServerErrorException('could not add auth')