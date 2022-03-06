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
    startTime: int
    endTime: int
    repeatCount: int
    bucketUrl: str
    member: Member

    layerId = db.Column('layer_id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sessionId = db.Column('session_id', UUID(as_uuid=True), db.ForeignKey('public.session.session_id'), nullable=False)
    memberId = db.Column('member_id', UUID(as_uuid=True), db.ForeignKey(Member.memberId), nullable=False)
    startTime = db.Column('startTime', db.Integer, nullable=False, default=0)
    endTime = db.Column('endTime', db.Integer, nullable=False, default=0)
    repeatCount = db.Column('repeat_count', db.Integer, nullable=False, default=1)
    bucketUrl = db.Column('bucket_url', db.String(520), nullable=True)
    member = db.relationship('Member', uselist=False, lazy='subquery')

    def __init__(self, sessionId, memberId, startTime, endTime, repeatCount, bucketUrl):
        self.sessionId = sessionId
        self.memberId = memberId
        self.startTime = startTime
        self.endTime = endTime
        self.repeatCount = repeatCount
        self.bucketUrl = bucketUrl

    def __repr__(self):
        return '<layer %s>' % str(self.layerId)

    __mapper_args__ = {
        'polymorphic_identity':'layer',
    }
