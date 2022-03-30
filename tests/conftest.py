import os
import tempfile
import pytest
from app.setup.setup import create_app

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
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

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