from socketio import Server
import os

sio = Server(cors_allowed_origins=[os.getenv('CORS_ORIGIN')], async_mode='threading')