from app.app import app
import eventlet

harmonyHub = app

if __name__ == '__main__':
    harmonyHub.run(threaded=True)