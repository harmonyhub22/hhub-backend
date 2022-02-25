from app.db.models.Genre import Genre

def getById(id):
    return Genre.query.get(id)

def getByName(name):
    return Genre.query.filter(name=name).first()

def getAll():
    return Genre.query.all()