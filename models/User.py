from sqlalchemy import null
from app import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class User(db.Model):
    __tablename__ = "USERS"

    userId = db.Column('USER_ID', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column('EMAIL', db.String(30), unique=True, nullable=False)
    firstname = db.Column('FIRST_NAME', db.String(30), unique=True, nullable=False)
    lastname = db.Column('LAST_NAME', db.String(30), unique=True, nullable=False)
    isOnline = db.Column('IS_ONLINE', db.Boolean, nullable=False)

    def __init__(self, email, firstname, lastname, isOnline = True):
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.isOnline = isOnline

    def __repr__(self):
        return '<User %s>' % str(self.userId)

    __mapper_args__ = {
        'polymorphic_identity':'user',
    }
