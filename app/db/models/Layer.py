from dataclasses import dataclass
import os
from app.db.db import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.models.Member import Member

@dataclass
class Layer(db.Model):

    __table_args__ = {'schema':os.getenv('SCHEMA', 'public')}

    layerId: uuid
    sessionId: uuid
    name: str
    startTime: float
    y: float
    duration: float
    fileName: str
    bucketUrl: str
    fadeInDuration: float
    fadeOutDuration: float
    isReversed: bool
    trimmedStartDuration: float
    trimmedEndDuration: float
    member: Member

    layerId = db.Column('layer_id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sessionId = db.Column('session_id', UUID(as_uuid=True), db.ForeignKey('public.session.session_id'), nullable=False)
    memberId = db.Column('member_id', UUID(as_uuid=True), db.ForeignKey(Member.memberId), nullable=False)
    name = db.Column('name', db.String(50), nullable=False, default="layer-name")
    startTime = db.Column('start_time', db.Float, nullable=False, default=0.0)
    y = db.Column('y', db.Float, default=0.0)
    duration = db.Column('duration', db.Float, nullable=False, default=0.0)
    fileName = db.Column('file_name', db.String(255), nullable=True)
    bucketUrl = db.Column('bucket_url', db.String(520), nullable=True)
    fadeInDuration = db.Column('fade_in_duration', db.Float, nullable=False, default=0.0)
    fadeOutDuration = db.Column('fade_out_duration', db.Float, nullable=False, default=0.0)
    isReversed = db.Column('reversed', db.Boolean, nullable=False, default=False)
    trimmedStartDuration = db.Column('trimmed_start_duration', db.Float, nullable=False, default=0.0)
    trimmedEndDuration = db.Column('trimmed_end_duration', db.Float, nullable=False, default=0.0)
    member = db.relationship('Member', uselist=False, lazy='subquery')

    def __init__(self, sessionId, memberId, name, startTime, duration, fadeInDuration, fadeOutDuration, isReversed, 
        trimmedStartDuration, trimmedEndDuration, bucketUrl=None, fileName=None, y=None):

        self.sessionId = sessionId
        self.memberId = memberId
        self.name = name
        self.startTime = startTime
        self.duration = duration
        self.fadeInDuration = fadeInDuration
        self.fadeOutDuration = fadeOutDuration
        self.isReversed = isReversed
        self.trimmedEndDuration = trimmedEndDuration
        self.bucketUrl = bucketUrl
        self.fileName = fileName
        self.y = y

    def __repr__(self):
        return '<layer %s>' % str(self.layerId)

    __mapper_args__ = {
        'polymorphic_identity':'layer',
    }
