import os
from app.app import app, sio

if __name__ == "__main__":
    print('in main')
    sio.run(app)