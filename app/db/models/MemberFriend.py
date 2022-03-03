from dataclasses import dataclass
import os
from app.db.db import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.db.models.Member import Member

@dataclass
class MemberFriend(db.Model):

    __table_args__ = {'schema':os.getenv('SCHEMA', 'public')}

    memberFriendId: uuid
    member1: Member
    member2: Member

    memberFriendId = db.Column('member_friend_id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    member1Id = db.Column('member_id', UUID(as_uuid=True), db.ForeignKey(Member.memberId), nullable=False)
    member2Id = db.Column('friend_id', UUID(as_uuid=True), db.ForeignKey(Member.memberId), nullable=False)
    member1 = db.relationship('Member', uselist=False, foreign_keys=[member1Id])
    member2 = db.relationship('Member', uselist=False, foreign_keys=[member2Id])

    def __init__(self, member1Id, member2Id):
        self.member1Id = member1Id
        self.member2Id = member2Id

    def __repr__(self):
        return '<member_friend %s-%s>' % str(self.member1Id), str(self.member2Id)

    __mapper_args__ = {
        'polymorphic_identity':'member_friend',
    }
