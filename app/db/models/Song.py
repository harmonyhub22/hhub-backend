from dataclasses import dataclass
import datetime
import os
from xmlrpc.client import DateTime
from app.db.db import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import func
import uuid
from app.db.db import db
from app.db.models.Member import Member

from app.db.models.Session import Session

@dataclass
class Song(db.Model):

    __table_args__ = {'schema':os.getenv('SCHEMA', 'public')}

    songId: uuid
    session: Session
    member: Member
    name: str
    duration: int
    createdAt: DateTime

    songId = db.Column('song_id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sessionId = db.Column('session_id', UUID(as_uuid=True), db.ForeignKey(Session.sessionId), nullable=False)
    memberId = db.Column('member_id', UUID(as_uuid=True), db.ForeignKey(Member.memberId), nullable=False)
    name = db.Column('name', db.String(30), nullable=False, default='My New Song')
    createdAt = db.Column('created_at', db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    session = db.relationship('Session', uselist=False, foreign_keys=[sessionId])
    member = db.relationship('Member', uselist=False, foreign_keys=[memberId])

    def __init__(self, sessionId, memberId, name):
        self.sessionId = sessionId
        self.memberId = memberId
        self.name = name

    def __repr__(self):
        return '<song %s>' % str(self.songId)

    __mapper_args__ = {
        'polymorphic_identity':'song',
    }