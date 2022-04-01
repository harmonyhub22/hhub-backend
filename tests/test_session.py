import pytest
from app.db.db import db
from app.db.models.Session import Session

'''
Route: api/session
REST operation: GET
Service method tested: getAllByMemberId()
Cases to test:
1. giving a session ID where no existing session has that ID (catch BadRequestException - no session with this ID)
2. giving a valid session ID but the logged in member is not in that session (catch BadRequestException - no session with this member)
3. normal case: valid session ID, member ID exists, queryset should have only 1 session. check metadata
'''
def testGetSession(app, client, auth):
    pass

'''
Route: api/session/live
REST operation: GET
Service method tested: getLiveSession()
Cases to test:
1. 
'''
def testGetLiveSession(app, client, auth):
    pass

'''
Route: api/session/<session ID>/end
REST operation: POST
Service method tested: endSession()
Cases to test:
1. no session is created, so you cant end one (catch BadRequestException)
2. member is not yet in a session, so cant end one (catch BadRequestException)
3. normal case: end a session the member is in. check that the session record has a properly updated end time
'''
def testEndSession(app, client, auth):
    pass