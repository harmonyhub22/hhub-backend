from app.app import app
from flask_socketio import SockketIO

awesome_app = app

if __name__ == '__main__':
    socketio.run(awesome_app)
    #awesome_app.run()