import sqlite3

import pytest

# TODO: change this code so that it works with out database set-up
# from flaskr.db import get_db


# def test_get_close_db(app):
#     with app.app_context():
#         db = get_db()
#         assert db is get_db()

#     with pytest.raises(sqlite3.ProgrammingError) as e:
#         db.execute('SELECT 1')

#     assert 'closed' in str(e.value)