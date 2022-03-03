import os
from app.app import app

awesomeapp = app

from app.socket.init import sio
import app.socket.endpoints # add all socket.io event listeners

if __name__ == '__main__':
    sio.run()