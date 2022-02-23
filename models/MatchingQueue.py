import datetime
from sqlalchemy import DateTime, null
from app import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.sql import func

class MatchingQueue(db.Model):
    __tablename__ = "MATCHING_QUEUES"

    matchingQueueId = db.Column('MATCHING_QUEUE_ID', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    userId = db.Column('USER_ID', UUID(as_uuid=True), db.ForeignKey('USERS.USER_ID'), nullable=False)
    timeEntered = db.Column('TIME_ENTERED', DateTime(timezone=True), nullable=False, server_default=func.now())
    user = db.relationship("User", uselist=False)

    def __init__(self, userId):
        self.userId = userId

    def __repr__(self):
        return '<MatchingQueue %s>' % str(self.matchingQueueId)

    __mapper_args__ = {
        'polymorphic_identity':'userFriend',
    }
