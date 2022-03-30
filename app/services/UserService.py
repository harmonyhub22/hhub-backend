from app.db.models.Auth import User
from sqlalchemy import func
from app.db.db import db
from app.exceptions.ServerErrorException import ServerErrorException
from app.exceptions.UnauthorizedException import UnauthorizedException

def getAll():
    return User.query.all()

def getUserName(userName):
    return User.query.filter(User.userName == userName).first()

def getUserID(userID):
    return User.query.filter(User.userID == userID).first()

def addUser(userName, password):
    try:
        user = User(userName, password)
        print("The user is", user)
        db.session.add(user)
        db.session.commit()
        return user
    except Exception:
        db.session.rollback()
        raise ServerErrorException('could not add user')