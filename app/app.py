from app.setup.setup import create_app

def getApps(test_config=None):
    print("here")
    app, sio = create_app(test_config)
    return app, sio
