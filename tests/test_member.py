import pytest
from app.db.db import db
from app.db.models.Member import Member
from app.services.AuthService import generateToken, getByMemberId as getByMemberIdAuth
import uuid
'''
Route: api/members/<member ID>
REST operation: GET
Service method tested: getById()
Cases to test:
1. trying to get a member with an invalid member ID. check that queryset is empty
2. normal case: valid member ID 
'''
def testGetMemberById(client, app, auth):
    auth.login()

    deanId = uuid.UUID('28cf2179-74ed-4fab-a14c-3c09bd904365')
    willId = uuid.UUID('73f80e58-bc0e-4d35-b0d8-d711a26299ac')

    with app.app_context():
        authMember = getByMemberIdAuth(deanId)
        token = generateToken(authMember.memberId)
        client.set_cookie(app, 'hhub-token', str(token))

    # case 1
    res = client.get('/api/members/28cf2179-74ed-0000-0000-3c09bd904365')
    assert res.data == b'null\n'

    # case 2
    deanId = uuid.UUID('28cf2179-74ed-4fab-a14c-3c09bd904365')
    res = client.get('/api/members/28cf2179-74ed-4fab-a14c-3c09bd904365')
    assert res is not None