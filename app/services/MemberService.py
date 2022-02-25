from app.db.models.Member import Member

def getById(id):
    return Member.query.get(id)

def getByFirstname(fn):
    return Member.query.filter(firstname=fn).first()

def getByLastname(ln):
    return Member.query.filter(lastname=ln).first()

def getByEmail(email):
    return Member.query.filter(email=email).first()

def getAll():
    return Member.query.all()