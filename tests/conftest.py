import os
import tempfile

import pytest
from app.setup.setup import create_app

# @pytest.fixture annotation tells pytest that the following function creates (using the yield command) 
@pytest.fixture
def app():
    # make a temporary file, returning 
    db_fd, db_path = tempfile.mkstemp()

    # we can also configure temporary database files or set configurations for testing
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    yield app

    os.close(db_fd)
    os.unlink(db_path)

# Tests will use this client to make requests to the application without running the server
@pytest.fixture
def client(app):
    return app.test_client()

# the runner fixture creates a runner that can call the Click commands registered with the application
@pytest.fixture
def runner(app):
    return app.test_cli_runner()