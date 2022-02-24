import os
from app.db.db import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Member(db.Model):

    #__table_args__ = {'schema':os.getenv('SCHEMA', 'hhub')}

    memberId = db.Column('member_id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column('email', db.String(30), unique=True, nullable=False)
    firstname = db.Column('first_name', db.String(30), unique=True, nullable=False)
    lastname = db.Column('last_name', db.String(30), unique=True, nullable=False)
    isOnline = db.Column('is_online', db.Boolean, nullable=False)

    def __init__(self, email, firstname, lastname, isOnline = True):
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.isOnline = isOnline

    def __repr__(self):
        return '<member %s>' % str(self.memberId)

    __mapper_args__ = {
        'polymorphic_identity':'member',
    }
