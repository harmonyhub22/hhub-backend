from sqlalchemy import null
from app import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Genre(db.Model):
    __tablename__ = "GENRES"

    genreId = db.Column('GENRE_ID', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column('NAME', db.String(20), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Genre %s>' % str(self.genreId)

    __mapper_args__ = {
        'polymorphic_identity':'genre',
    }
