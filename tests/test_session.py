import pytest
from app.db.db import db
from app.db.models.Session import Session

'''
route: api/session/<sessionID>/layers/<layerID>
REST operation: GET
service method tested: getAllByMemberId()

cases to test:
- when the member ID is 
'''
def testGetSession(app, client, auth):
    pass


