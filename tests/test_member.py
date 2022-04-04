import pytest
from app.db.db import db
from app.db.models.Member import Member
import uuid
'''
Route: api/members/<member ID>
REST operation: GET
Service method tested: getById()
Cases to test:
1. trying to get a member with an invalid member ID. check that queryset is empty
2. normal case: valid member ID 
'''
def testGetMemberById(client, app,auth):
    auth.login()
    #case 1
    nullid = uuid.UUID('28cf2179-74ed-0000-0000-3c09bd904365')
    with app.app_context():
        query = Member.query.get(nullid)
        assert not query
    #case 2
    deanId = uuid.UUID('28cf2179-74ed-4fab-a14c-3c09bd904365')
    with app.app_context():
        query = Member.query.get(deanId)
        assert len(query) == 1
        assert query[0].member_id == 0
    pass