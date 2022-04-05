import json
import uuid
from flask import session
import pytest
from app.services.AuthService import getByMemberId as getByMemberIdAuth
from app.services.MemberService import getByEmail


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
    # check for the correct route
    assert client.get('/api/signup').status_code == 200
    client.post('/api/signup', 
                           data={'email': 'a', 'firstname': 'a', 'lastname': 'a', 'password': 'a'})
    
@pytest.mark.parametrize(('email', 'firstname', 'lastname', 'password', 'message'), (
    ('', '', '', '', b'email is required.'),
    ('a', '', 'a', 'a', b'firstname is required.'),
    ('a', 'a', '', 'a', b'lastname is required.'),
    ('a', 'a', 'a', '', b'password is required.'),
    ('a', 'a', 'a', 'a', b'account is already registered'),
))
def test_register_validate_input(client, email, firstname, lastname, password, message):
    response = client.post(
        '/api/signup',
        data={'email': email,  'firstname': firstname, 'lastname': lastname, 'password': password}
    )
    assert message in response.data
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
def testLogin(client, auth):
    #client.set_cookie()
    assert client.get('/api/login').status_code == 200
    auth.login()
    memberId = uuid.UUID('0dfedda5-ddd3-481f-90d9-6ee388c4093e')
    email = "vitruong00@tamu.edu"
    password = "password"
    
    auth.login()
    with client:
        client.get('/')
        member = getByEmail(email)
        authMember = getByMemberIdAuth(memberId)
        assert member.email == email
        assert authMember.password == password

@pytest.mark.parametrize(('email', 'password', 'message'), (
('a', "password", b'Incorrect email.'),
('vitruong00@tamu.edu', 'a', b'Incorrect password.'),
))
def test_login_validate_input(auth, email, password, message):
    response = auth.login(email, password)
    assert message in response.data

'''
Route: api/logout
REST operation: POST
Service methods tested: none (just deletes cookie)
Cases to test:
1. normal logout. check 200 response
'''
@pytest.mark.order(3)
def testLogout(client, auth):
    auth.login()
    email = "vitruong00@tamu.edu"
    
    with client:
        member = getByEmail(email)
        auth.logout()
        assert member.memberId not in session