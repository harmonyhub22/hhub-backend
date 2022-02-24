import os
from sqlalchemy import DateTime
from app.db.db import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.sql import func

from app.db.models.Member import Member

class MatchingQueue(db.Model):

    __table_args__ = {'schema':os.getenv('SCHEMA', 'hhub')}

    matchingQueueId = db.Column('matching_queue_id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    memberId = db.Column('member_id', UUID(as_uuid=True), db.ForeignKey(Member.memberId), nullable=False)
    timeEntered = db.Column('time_entered', DateTime(timezone=True), nullable=False, server_default=func.now())
    member = db.relationship("Member", uselist=False)

    def __init__(self, memberId):
        self.memberId = memberId

    def __repr__(self):
        return '<matching_queue %s>' % str(self.matchingQueueId)

    __mapper_args__ = {
        'polymorphic_identity':'matching_queue',
    }
