import os

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') if os.environ.get('DATABASE_URL').startswith("postgresql://") else os.environ.get('DATABASE_URL').replace("postgres://", "postgresql://", 1)
SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS', False)