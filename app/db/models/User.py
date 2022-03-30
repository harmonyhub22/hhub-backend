from dataclasses import dataclass
from enum import unique
import os
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.db import db
from  werkzeug.security import generate_password_hash, check_password_hash

@dataclass
class User(db.Model):
    
    userID: uuid
    userName: str
    password: str
    
    __table_args__ = {'schema':os.getenv('SCHEMA', 'public')} 
    
    userID = db.Column('user_id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    userName = db.Column('user_name', db.String(64), unique=True)
    password = db.Column('password',db.String(128))
    
    def __init__(self, userName, password):
        self.userName = userName
        self.password = password
    
    
    def __repr__(self):
        return '<user %s>' % str(self.userID)

    __mapper_args__ = {
        'polymorphic_identity':'user',
    }
