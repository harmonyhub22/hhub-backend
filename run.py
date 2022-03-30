import os
from app.app import getApps

if __name__ == "__main__":
    app, sio = getApps()
    sio.run(app)