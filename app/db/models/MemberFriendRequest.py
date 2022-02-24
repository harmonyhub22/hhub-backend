import os
from app.db.db import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.db.models.Member import Member

class MemberFriendRequest(db.Model):

    #__table_args__ = {'schema':os.getenv('SCHEMA', 'hhub')}

    memberFriendId = db.Column('memeber_friend_request_id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    memberId = db.Column('memebr_id', UUID(as_uuid=True), db.ForeignKey(Member.memberId), nullable=False)
    friendId = db.Column('friend_id', UUID(as_uuid=True), db.ForeignKey(Member.memberId), nullable=False)
    member = db.relationship('Member', uselist=False, foreign_keys=[memberId])
    friend = db.relationship('Member', uselist=False, foreign_keys=[friendId])

    def __init__(self, memberId, friendId):
        self.memberId = memberId
        self.friendId = friendId

    def __repr__(self):
        return '<member_friend_request %s-%s>' % str(self.memberId), str(self.friendId)

    __mapper_args__ = {
        'polymorphic_identity':'member_friend_request',
    }