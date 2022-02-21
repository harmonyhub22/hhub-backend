from sqlalchemy import null
from app import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Layer(db.Model):
    __tablename__ = "LAYERS"

    layerId = db.Column('LAYER_ID', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sessionId = db.Column('SESSION_ID', UUID(as_uuid=True), db.ForeignKey('SESSIONS.SESSION_ID'), nullable=False)
    startMeasure = db.Column('START_MEASURE', db.Integer, nullable=False)
    repeatCount = db.Column('REPEAT_COUNT', db.Integer, nullable=False, default=0)
    bucketUrl = db.Column('BUCKET_URL', db.String(520), nullable=False)
    session = db.relationship('Session', lazy=True, uselist=False)

    def __init__(self, sessionId, startMeasure, repeatCount, bucketUrl):
        self.sessionId = sessionId
        self.startMeasure = startMeasure
        self.repeatCount = repeatCount
        self.bucketUrl = bucketUrl

    def __repr__(self):
        return '<Layer %s>' % str(self.layerId)

    __mapper_args__ = {
        'polymorphic_identity':'layer',
    }
