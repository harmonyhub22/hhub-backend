import pytest

# note: we should wait until password stuff is merged into master before testing auth

'''
Route: api/signup
REST operation: POST
Service method tested: addMember()
Cases to test:
'''
def testSignup(client):
    pass

'''
Route: api/login
REST operation: POST
Service method tested: addMember()
Cases to test:
'''
def testLogin(client):
    pass

def testLogout(client, auth):
    pass
    '''
    auth.login()

    with client:
        auth.logout()
        # TODO: what are we checking?
    '''