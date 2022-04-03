from dataclasses import dataclass
from enum import unique
import os
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.db import db
from app.db.models.Member import Member

@dataclass
class Auth(db.Model):
    
    authId: uuid
    memberId: uuid
    password: str
    
    __table_args__ = {'schema':os.getenv('SCHEMA', 'public')} 
    
    authId = db.Column('auth_id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    memberId = db.Column('member_id', UUID(as_uuid=True), db.ForeignKey(Member.memberId), default=uuid.uuid4)
    password = db.Column('password', db.String(128))
    
    def __init__(self, memberId, password):
        self.memberId = memberId
        self.password = password
    
    
    def __repr__(self):
        return '<auth %s>' % str(self.authId)

    __mapper_args__ = {
        'polymorphic_identity':'auth',
    }
