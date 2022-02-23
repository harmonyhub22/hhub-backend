class Test(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        print("You are here")
        return self.app(environ, start_response)