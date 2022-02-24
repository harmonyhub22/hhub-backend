import os
from app.db.db import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Genre(db.Model):

    #__table_args__ = {'schema':os.getenv('SCHEMA', 'hhub')}

    genreId = db.Column('genre_id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column('name', db.String(20), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<genre %s>' % str(self.genreId)

    __mapper_args__ = {
        'polymorphic_identity':'genre',
    }
