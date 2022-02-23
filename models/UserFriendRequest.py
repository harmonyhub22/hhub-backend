from sqlalchemy import null
from app import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class UserFriendRequest(db.Model):
    __tablename__ = "USER_FRIEND_REQUESTS"

    userFriendId = db.Column('USER_FRIEND_REQUEST_ID', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    userId = db.Column('USER_ID', UUID(as_uuid=True), db.ForeignKey('USERS.USER_ID'), nullable=False)
    friendId = db.Column('FRIEND_ID', UUID(as_uuid=True), db.ForeignKey('USERS.USER_ID'), nullable=False)
    user = db.relationship('User', uselist=False, foreign_keys=[userId])
    friend = db.relationship('User', uselist=False, foreign_keys=[friendId])

    def __init__(self, userId, friendId):
        self.userId = userId
        self.friendId = friendId

    def __repr__(self):
        return '<UserFriendRequests %s-%s>' % str(self.userId), str(self.friendId)

    __mapper_args__ = {
        'polymorphic_identity':'userFriendRequest',
    }