from dataclasses import dataclass
import os
from app.db.db import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.db.models.Session import Session

@dataclass
class Layer(db.Model):

    __table_args__ = {'schema':os.getenv('SCHEMA', 'hhub')}

    layerId: uuid
    #session: Session
    startMeasure: int
    repeatCount: int
    bucketUrl: str

    layerId = db.Column('layer_id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sessionId = db.Column('session_id', UUID(as_uuid=True), db.ForeignKey(Session.sessionId), nullable=False)
    startMeasure = db.Column('start_measure', db.Integer, nullable=False, default=0)
    repeatCount = db.Column('repeat_count', db.Integer, nullable=False, default=1)
    bucketUrl = db.Column('bucket_url', db.String(520), nullable=False)

    def __init__(self, sessionId, startMeasure, repeatCount, bucketUrl):
        self.sessionId = sessionId
        self.startMeasure = startMeasure
        self.repeatCount = repeatCount
        self.bucketUrl = bucketUrl

    def __repr__(self):
        return '<layer %s>' % str(self.layerId)

    __mapper_args__ = {
        'polymorphic_identity':'layer',
    }
