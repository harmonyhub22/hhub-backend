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

    __table_args__ = {'schema':os.getenv('SCHEMA', 'hhub')}

    songId: uuid
    session: Session
    name: str
    duration: int
    bucketUrl: str
    createdAt: DateTime
    tempo: int
    #numLikes: int

    songId = db.Column('song_id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sessionId = db.Column('session_id', UUID(as_uuid=True), db.ForeignKey(Session.sessionId), nullable=False)
    name = db.Column('name', db.String(30), nullable=False, default='My New Song')
    duration = db.Column('duration', db.Integer, default=60)
    bucketUrl = db.Column('bucket_url', db.String(520), nullable=False)
    createdAt = db.Column('created_at', db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    tempo = db.Column('tempo', db.Integer, default=120)
    session = db.relationship('Session', uselist=False, foreign_keys=[sessionId])

    '''
    @hybrid_property
    def numLikes(self):
        return self.numLikesExpression(self)

    @numLikes.expression
    def numLikesExpression(cls):
        return db.session.query(func.count('likes')).\
            filter_by('likes.song_id'==cls.songId).\
            label('numLikes')
    '''


    def __init__(self, sessionId, name, duration, bucketUrl, tempo = 120):
        self.sessionId = sessionId
        self.name = name
        self.duration = duration
        self.bucketUrl = bucketUrl
        self.tempo = tempo

    def __repr__(self):
        return '<song %s>' % str(self.songId)

    __mapper_args__ = {
        'polymorphic_identity':'song',
    }

likes = db.Table('likes',
    db.Column('song_id', UUID(as_uuid=True), db.ForeignKey(Song.songId), primary_key=True),
    db.Column('member_id', UUID(as_uuid=True), db.ForeignKey(Member.memberId), primary_key=True)
)