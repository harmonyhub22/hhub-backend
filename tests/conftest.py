import os
import tempfile
import pytest

# we must add the root dir to the python path in order for pytest to see app/app.py
import sys
from os.path import dirname as d
from os.path import abspath, join
root_dir = d(d(abspath(__file__)))
sys.path.append(root_dir)
from app.app import getApps

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, email='dean27@tamu.edu', firstname='Dean', lastname='Something'):
        return self._client.post(
            '/api/login',
            data={'email': email, 'firstname': firstname, 'lastname': lastname}
        )

    def logout(self):
        return self._client.get('/api/logout')

# @pytest.fixture annotation tells pytest that the following function creates (using the yield command) 
@pytest.fixture
def app():
    # make a temporary file, returning the file descriptor and path to it
    db_fd, db_path = tempfile.mkstemp()

    # we can also configure temporary database files or set configurations for testing
    app, sio = getApps({
        'TESTING': True,
        'DATABASE': db_path,
    })
    # app = create_app({
    #     'TESTING': True,
    #     'DATABASE': db_path,
    # })

    yield app

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def auth(client):
    return AuthActions(client)