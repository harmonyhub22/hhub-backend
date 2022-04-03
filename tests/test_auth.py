import pytest

'''
Route: api/signup
REST operation: POST
Service methods tested: addMember(), getByMemberId(), addOrUpdateAuth(), generateToken()
Cases to test:
1. no email provided (catch 400 error)
2. no password provided (catch 400 error)
3. if user is not a member, create them and authenticate them. check queryset and hhub-token
4. is a member and tries signing up again, so it logs them in. check 200 response
'''
@pytest.mark.order(1)
def testSignup(client):
    data = {
        'email': '',
        'firstname': '',
        'lastname': '',
        'password': '',
    }
    pass

'''
Route: api/login
REST operation: PUT
Service methods tested: getByMemberId(), generateToken()
Cases to test:
1. email is not provided (catch 400 error)
2. password is not provided (catch 400 error)
3. no info is provided (catch 400 error)
4. invalid username provided (catch 400 error)
5. invalid password provided (catch 400 error)
5. normal case: correct info provided. check 200 response
'''
@pytest.mark.order(2)
def testLogin(client):
    #client.set_cookie()
    pass

'''
Route: api/logout
REST operation: POST
Service methods tested: none (just deletes cookie)
Cases to test:
1. normal logout. check 200 response
'''
@pytest.mark.order(3)
def testLogout(client, auth):
    pass
    '''
    auth.login()

    with client:
        auth.logout()
        assert
    '''