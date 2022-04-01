import pytest
from app.db.db import db
from app.db.models.Member import Member

'''
Route: api/members/<member ID>
REST operation: GET
Service method tested: getById()
Cases to test:
1. trying to get a member with an invalid member ID. check that queryset is empty
2. normal case: valid member ID 
'''
def testGetMemberById(client, app):
    pass