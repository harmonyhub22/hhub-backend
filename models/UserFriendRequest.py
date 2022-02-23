from sqlalchemy import null
from app import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class UserFriendRequest(db.Model):
    __tablename__ = "USER_FRIEND_REQUESTS"

    userId = db.Column('USER_ID', UUID(as_uuid=True), db.ForeignKey('USERS.USER_ID'), primary_key=True)
    friendId = db.Column('FRIEND_ID', UUID(as_uuid=True), db.ForeignKey('USERS.USER_ID'), primary_key=True)
    user = db.relationship('User', uselist=False)
    friend = db.relationship('User', uselist=False)

    def __init__(self, userId, friendId):
        self.userId = userId
        self.friendId = friendId

    def __repr__(self):
        return '<UserFriendRequests %s>' % str(self.friendId)

    __mapper_args__ = {
        'polymorphic_identity':'userFriendRequest',
    }