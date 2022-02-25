from app.db.models.Genre import Genre
from sqlalchemy import func

def getById(id):
    return Genre.query.get(id)

def getByName(name):
    return Genre.query.filter(func.lower(Genre.name)==func.lower(name)).first()

def getAll():
    return Genre.query.all()