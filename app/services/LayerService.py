from app.db.models.Layer import Layer

def getById(id):
    return Layer.query.get(id)

def getAllBySessionId(sessionId):
    return Layer.query.filter(sessionId=sessionId)
