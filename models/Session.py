import datetime
from sqlalchemy import null
from app import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Session(db.Model):
    __tablename__ = "SESSIONS"

    sessionId = db.Column('SESSION_ID', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    genreId = db.Column('GENRE_ID', UUID(as_uuid=True), db.ForeignKey('GENRES.GENRE_ID'), nullable=False)
    user1Id = db.Column('USER1_ID', UUID(as_uuid=True), db.ForeignKey('USERS.USER_ID'), nullable=False)
    user2Id = db.Column('USER2_ID', UUID(as_uuid=True), db.ForeignKey('USERS.USER_ID'), nullable=False)
    turnCount = db.Column('TURN_COUNT', db.Integer, nullable=False, default=0)
    startTime = db.Column('START_TIME', db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    endTime = db.Column('END_TIME', db.DateTime)
    genre = db.relationship('Genre')
    user1 = db.relationship('User', uselist=False, foreign_keys=[user1Id])
    user2 = db.relationship('User', uselist=False, foreign_keys=[user2Id])
    layers = db.relationship('Layer', backref='session', lazy=True, uselist=True)

    def __init__(self, genreId, user1Id, user2Id):
        self.genreId = genreId
        self.user1Id = user1Id
        self.user2Id = user2Id

    def __repr__(self):
        return '<Session %s>' % str(self.sessionId)

    __mapper_args__ = {
        'polymorphic_identity':'session',
    }
