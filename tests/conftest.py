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