import json
from re import M
import uuid
import pytest
from app.services.MemberService import getByEmail as getMemberByEmail, addMember
from app.services.AuthService import getByMemberId as getAuthByMemberId, addOrUpdateAuth
from app.services.AuthService import generateToken
from app.exceptions.ServerErrorException import ServerErrorException

'''
Route: api/signup
REST operation: POST
Service methods tested: addMember(), getByMemberId(), addOrUpdateAuth(), generateToken()
Cases to test:
1. normal sign up (no user exists with email, all info provided). check that query is not None
2. no info at all is provided. check 400 error message
3. no first name provided. check 400 error message
4. no last name provided. check 400 error message
5. no password provided. check 400 error message
6. no email provided. check 400 error message
7. trying to sign up with an email thats already taken. check 400 error message
'''
def testSignup(app, client):
    # case 1
    response = client.post(
        '/api/signup', 
        data=json.dumps({'email': 'a', 'firstname': 'a', 'lastname': 'a', 'password': 'a'}),
        headers={"Content-Type": "application/json"}
    )
    jsonResponse = json.loads(response.data.decode('utf-8'))
    assert jsonResponse['success'] == True

    with app.app_context():
        user = getMemberByEmail('a')
        assert user != None
    
    # case 2
    response = client.post(
        '/api/signup',
        data=json.dumps({'email': '',  'firstname': '', 'lastname': '', 'password': ''}),
        headers={"Content-Type": "application/json"})
    jsonResponse = json.loads(response.data.decode('utf-8'))
    assert 'Please provide your email' in jsonResponse['reason']

    # case 3
    response = client.post(
        '/api/signup',
        data=json.dumps({'email': 'a',  'firstname': '', 'lastname': 'a', 'password': 'a'}),
        headers={"Content-Type": "application/json"})
    jsonResponse = json.loads(response.data.decode('utf-8'))
    assert 'Please provide your first and last name' in jsonResponse['reason']

    # case 4
    response = client.post(
        '/api/signup',
        data=json.dumps({'email': 'a',  'firstname': 'a', 'lastname': '', 'password': 'a'}),
        headers={"Content-Type": "application/json"})
    jsonResponse = json.loads(response.data.decode('utf-8'))
    assert 'Please provide your first and last name' in jsonResponse['reason']

    # case 5
    response = client.post(
        '/api/signup',
        data=json.dumps({'email': 'a',  'firstname': 'a', 'lastname': 'a', 'password': ''}),
        headers={"Content-Type": "application/json"})
    jsonResponse = json.loads(response.data.decode('utf-8'))
    assert 'Please provide a password' in jsonResponse['reason']

    # case 6
    response = client.post(
        '/api/signup',
        data=json.dumps({'email': '',  'firstname': 'a', 'lastname': 'a', 'password': 'a'}),
        headers={"Content-Type": "application/json"})
    jsonResponse = json.loads(response.data.decode('utf-8'))
    assert 'Please provide your email' in jsonResponse['reason']

    # case 7
    response = client.post(
        '/api/signup',
        data=json.dumps({'email': 'a',  'firstname': 'a', 'lastname': 'a', 'password': 'a'}),
        headers={"Content-Type": "application/json"})
    jsonResponse = json.loads(response.data.decode('utf-8'))
    assert 'Member with this email already exists' in jsonResponse['reason']
    
def testSignupAddMember(app):
    email = "jennie@gmail.com"
    firstname = "Jennie"
    lastname = "Kim"
    with app.app_context():
        member = addMember(email, firstname, lastname)
        assert member is not None
        
def testSignupWithInvalidMember(app):
    email = "jennie@gmail.com"
    with app.app_context():
        member = getMemberByEmail(email)
        assert member is None

def testSignupWithAuthMember(app):
    memberId = uuid.UUID('0dfedda5-ddd3-481f-90d9-6ee388c4093e')
    with app.app_context():
        authMember = getAuthByMemberId(memberId)
        assert authMember is not None
        
def testSignupWithNoneAuthMember(app):
    email = "jennie@gmail.com"
    firstname = "Jennie"
    lastname = "Kim"
    with app.app_context():
        member = addMember(email, firstname, lastname)
        authMember = getAuthByMemberId(member.memberId)
        assert authMember is None
        
def testSignupWithAddOrUpdateAuth(app):
    email = "jennie@gmail.com"
    firstname = "Jennie"
    lastname = "Kim"
    password = "password"
    with app.app_context():
        member = addMember(email, firstname, lastname)
        authMember = addOrUpdateAuth(member.memberId, password)
        assert authMember is not None

def testSignupWithGenerateToken(app):
    memberId = uuid.UUID('0dfedda5-ddd3-481f-90d9-6ee388c4093e')
    with app.app_context():
        token = generateToken(memberId)
        assert token is not None
    
def testSignupWithGenerateTokenForNoneMember(app):
    email = "jennie@gmail.com"
    firstname = "Jennie"
    lastname = "Kim"
    password = "password"
    with app.app_context():
        member = addMember(email, firstname, lastname)
        authMember = addOrUpdateAuth(member.memberId, password)
        token = generateToken(authMember.memberId)
        assert token is not None


def testLogin(auth):
    response = auth.login()
    jsonResponse = json.loads(response.data.decode('utf-8'))
    assert jsonResponse['success'] == True

@pytest.mark.parametrize(('email', 'password', 'message'), (
('', 'a', 'Please provide your email.'),
('vitruong00@tamu.edu', '', 'Please provide a password.'),
('a', 'password', 'Account does not exist or incorrect. Please create an account first!'),
('a', 'a', 'Account does not exist or incorrect. Please create an account first!'),
('vitruong00@tamu.edu', 'a', 'Incorrect password!'),
))
def testLoginValidateInput(auth, email, password, message):
    response = auth.login(email, password)
    jsonResponse = json.loads(response.data.decode('utf-8'))
    assert message == jsonResponse['reason']
    
    
def testLoginWithValidateMember(app, auth):
    email = "vitruong00@tamu.edu"
    auth.login(email)
    with app.app_context():
        member = getMemberByEmail(email)
        assert member is not None

def testLoginWithInvalidMember(app, auth):
    email = "jennie@gmail.com"
    auth.login(email)   
    with app.app_context():
        member = getMemberByEmail(email)
        assert member is None
        
def testLoginWithValidAuthMember(app, auth):
    auth.login()
    email = "vitruong00@tamu.edu"
    with app.app_context():
        member = getMemberByEmail(email)
        authMember = getAuthByMemberId(member.memberId)
        assert authMember is not None
        
def testLoginWithNoneMember(app, auth):
    email = "jennie@gmail.com"
    with app.app_context():
        member = getMemberByEmail(email)
        if member is None:
            response = auth.login(email)
            jsonResponse = json.loads(response.data.decode('utf-8'))
            assert 'Account does not exist or incorrect. Please create an account first!' == jsonResponse['reason']