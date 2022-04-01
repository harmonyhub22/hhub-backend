import pytest
from app.db.db import db
from app.db.models.Member import Member

'''
Route: api/member
REST operation: GET
Service method tested: getAll()
Cases to test:
1. no accounts yet created, so queryset is empty
2. create an account, so queryset has 1 member. check email, name, and password
3. create another account, so queryset has 2 member. check email, name, and password
'''
def testGetAllMembers(client, app):
    pass

