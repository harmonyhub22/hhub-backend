from app.db.models.Session import Session

def getById(id):
    return Session.query.get(id)

def getByUserId(userId):
    return Session.query.filter((Session.user1Id==userId) | (Session.user2Id==userId)).first()

def getAll():
    return Session.query.all()