import os
from app.app import app

harmonyHub = app

from app.socket.init import sio
import app.socket.endpoints # add all socket.io event listeners

domain = os.getenv('SERVER_DOMAIN', 'http://localhost')
port = os.getenv('SERVER_PORT', 5000)

if __name__ == '__main__':
    sio.run(host=domain, port=port)