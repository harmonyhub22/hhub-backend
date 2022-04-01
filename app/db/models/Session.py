from dataclasses import dataclass, field
import datetime
import os
from typing import List
from xmlrpc.client import DateTime
from app.db.db import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.db.models.Genre import Genre
from app.db.models.Layer import Layer
from app.db.models.Member import Member

@dataclass
class Session(db.Model):

    __table_args__ = {'schema':os.getenv('SCHEMA', 'public')}

    sessionId: uuid
    startTime: DateTime
    endTime: DateTime
    member1: Member
    member2: Member
    bucketUrl: str
    layers: List[Layer] = field(default_factory=list)

    sessionId = db.Column('session_id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    genreId = db.Column('genre_id', UUID(as_uuid=True), db.ForeignKey(Genre.genreId), nullable=False)
    member1Id = db.Column('member1_id', UUID(as_uuid=True), db.ForeignKey(Member.memberId), nullable=False)
    member2Id = db.Column('member2_id', UUID(as_uuid=True), db.ForeignKey(Member.memberId), nullable=False)
    startTime = db.Column('start_time', db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    endTime = db.Column('end_time', db.DateTime)
    member1 = db.relationship('Member', uselist=False, foreign_keys=[member1Id])
    member2 = db.relationship('Member', uselist=False, foreign_keys=[member2Id])
    layers = db.relationship('Layer', backref='session', lazy='subquery', uselist=True, primaryjoin="Session.sessionId == Layer.sessionId")
    bucketUrl = db.Column('bucket_url', db.String(520), nullable=False)

    def __init__(self, genreId, member1Id, member2Id):
        self.genreId = genreId
        self.member1Id = member1Id
        self.member2Id = member2Id

    def __repr__(self):
        return '<session %s>' % str(self.sessionId)

    __mapper_args__ = {
        'polymorphic_identity':'session',
    }
