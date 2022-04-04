import pytest
from app.db.db import db
from app.db.models.Session import Session
import uuid
from app.exceptions.BadRequestException import BadRequestException

from app.services.AuthService import getByMemberId
'''
Route: api/session
REST operation: GET
Service method tested: getAllByMemberId()
Cases to test:
1. giving a session ID where no existing session has that ID (catch BadRequestException - no session with this ID)
2. giving a valid session ID but the logged in member is not in that session (catch BadRequestException - no session with this member)
3. normal case: valid session ID, member ID exists, queryset should have only 1 session. check metadata
'''
@pytest.mark.order(2)
def testGetSession(app, client, auth):
    # auth.login()
    # #case 1
    # nullId = uuid.UUID('28cf2179-74ed-0000-a14c-3c09bd904365')
    # with pytest.raises(BadRequestException) as info:
    #     record = client.get('api/session', data = {
    #         nullId
    #     })
    # assert "no session with this ID" in str(info.value)

    # #case 2 
    # deanId = uuid.UUID('28cf2179-74ed-4fab-a14c-3c09bd904365')
    # with pytest.raises(BadRequestException) as info:
    #     record = client.get('api/session', data = {
    #         'memberid': deanId
    #     })
    # assert "no session with this member" in str(info.value)

    #case 3
    

    pass


'''
Route: api/session/live
REST operation: GET
Service method tested: getLiveSession()
Cases to test:
1. 
'''
@pytest.mark.order(2)
def testGetLiveSession(app, client, auth):
    # auth.login()
    # #test = 'b52d3f89-b5a6-43e9-b352-4161a273e659'
    # #case 1
    # deanId = uuid.UUID('28cf2179-74ed-4fab-a14c-3c09bd904365')
    # with pytest.raises(BadRequestException) as info:
    #     checkSession = client.get('/api/sessions', data = {'MEMBERID': deanId})
    # assert str(info.value)
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