import pytest

'''
Route: api/signup
REST operation: POST
Service methods tested: addMember(), getByMemberId(), addOrUpdateAuth(), generateToken()
Cases to test:
1. if user is not a member, create them and authenticate them. check queryset and hhub-token
2. user is a member and tries signing up again, so they must log in (catch BadRequestException)
'''
@pytest.mark.order(1)
def testSignup(client):
    assert client.get()
    pass

'''
Route: api/login
REST operation: PUT
Service methods tested: getByMemberId(), generateToken()
Cases to test:
1. email is not provided 
2. 
'''
@pytest.mark.order(2)
def testLogin(client):
    pass

'''
Route: api/logout
REST operation: POST
Service methods tested: none (just deletes cookie)
Cases to test:
1. normal logout, assert 200 response
'''
@pytest.mark.order(3)
def testLogout(client, auth):
    pass
    '''
    auth.login()

    with client:
        auth.logout()
        # TODO: what are we checking?
    '''