from sqlalchemy import null
from app import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class UserFriend(db.Model):
    __tablename__ = "USER_FRIENDS"

    userFriendId = db.Column('USER_FRIEND_ID', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user1Id = db.Column('USER_ID', UUID(as_uuid=True), db.ForeignKey('USERS.USER_ID'), nullable=False)
    user2Id = db.Column('FRIEND_ID', UUID(as_uuid=True), db.ForeignKey('USERS.USER_ID'), nullable=False)
    user1 = db.relationship('User', uselist=False, foreign_keys=[user1Id])
    user2 = db.relationship('User', uselist=False, foreign_keys=[user2Id])

    def __init__(self, user1Id, user2Id):
        self.user1Id = user1Id
        self.user2Id = user2Id

    def __repr__(self):
        return '<UserFriends %s-%s>' % str(self.user1Id), str(self.user2Id)

    __mapper_args__ = {
        'polymorphic_identity':'userFriend',
    }
