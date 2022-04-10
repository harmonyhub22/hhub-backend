import datetime
import os
from app.db.models.Auth import Auth
from app.db.db import db
from app.exceptions.ServerErrorException import ServerErrorException
from app.exceptions.UnauthorizedException import UnauthorizedException
import jwt
from datetime import datetime, timedelta

def generateToken(memberId):
    secret = os.environ.get("SECRET_KEY", None)
    if secret == None:
        raise Exception
    
    token = jwt.encode({
        'memberId': str(memberId),
        'exp' : datetime.utcnow() + timedelta(minutes=1440)
    }, secret
    #, "HS256"
    ).decode('utf-8')

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
            return newAuth
        else:
            auth.password = password
            db.session.commit()

    except Exception:
        db.session.rollback()
        raise ServerErrorException('could not add auth')