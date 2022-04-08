import json
from re import M
import uuid
import pytest
from app.services.MemberService import getByEmail as getMemberByEmail, addMember
from app.services.AuthService import getByMemberId as getAuthByMemberId, addOrUpdateAuth
from app.services.AuthService import generateToken
from app.exceptions.ServerErrorException import ServerErrorException


# '''
# Route: api/signup
# REST operation: POST
# Service methods tested: addMember(), getByMemberId(), addOrUpdateAuth(), generateToken()
# Cases to test:
# 1. no email provided (catch 400 error)
# 2. no password provided (catch 400 error)
# 3. if user is not a member, create them and authenticate them. check queryset and hhub-token
# 4. is a member and tries signing up again, so it logs them in. check 200 response
# '''
# def testSignup(client):
#     # check for the correct route
#     response = client.post('/api/signup', 
#                            data=json.dumps({'email': 'a', 'firstname': 'a', 'lastname': 'a', 'password': 'a'}),
#                            headers={"Content-Type": "application/json"})
#     jsonResponse = json.loads(response.data.decode('utf-8'))
#     assert jsonResponse['success'] == True
    
# @pytest.mark.parametrize(('email', 'firstname', 'lastname', 'password', 'message'), (
#     ('', '', '', '', 'Please provide your email.'),
#     ('a', '', 'a', 'a', 'Please provide your first and last name.'),
#     ('a', 'a', '', 'a', 'Please provide your first and last name.'),
#     ('a', 'a', 'a', '', 'Please provide a password.'),
#     ('a', 'a', 'a', 'a', 'Account is already registered.'),
# ))
# def testSignupValidateInput(client, email, firstname, lastname, password, message):
#     response = client.post(
#         '/api/signup',
#         data=json.dumps({'email': email,  'firstname': firstname, 'lastname': lastname, 'password': password}),
#         headers={"Content-Type": "application/json"})
#     jsonResponse = json.loads(response.data.decode('utf-8'))
#     assert message == jsonResponse['reason']
    
# def testSignupAddMember(app):
#     email = "jennie@gmail.com"
#     firstname = "Jennie"
#     lastname = "Kim"
#     with app.app_context():
#         member = addMember(email, firstname, lastname)
#         assert member is not None
        
# def testSignupWithInvalidMember(app):
#     email = "jennie@gmail.com"
#     with app.app_context():
#         member = getMemberByEmail(email)
#         assert member is None
        
# # def testSignupAddExistingMember(app, auth):
# #     auth.login()
# #     email = "vitruong00@tamu.edu"
# #     firstname = "Vi"
# #     lastname = "Truong"
# #     with pytest.raises(ServerErrorException) as excinfo:
# #         addMember(email, firstname, lastname)
# #         assert "could not add member" in str(excinfo.value)

# def testSignupWithAuthMember(app):
#     memberId = uuid.UUID('0dfedda5-ddd3-481f-90d9-6ee388c4093e')
#     with app.app_context():
#         authMember = getAuthByMemberId(memberId)
#         assert authMember is not None
        
# def testSignupWithNoneAuthMember(app):
#     email = "jennie@gmail.com"
#     firstname = "Jennie"
#     lastname = "Kim"
#     with app.app_context():
#         member = addMember(email, firstname, lastname)
#         authMember = getAuthByMemberId(member.memberId)
#         assert authMember is None
        
# def testSignupWithAddOrUpdateAuth(app):
#     email = "jennie@gmail.com"
#     firstname = "Jennie"
#     lastname = "Kim"
#     password = "password"
#     with app.app_context():
#         member = addMember(email, firstname, lastname)
#         authMember = addOrUpdateAuth(member.memberId, password)
#         assert authMember is not None

# def testSignupWithGenerateToken(app):
#     memberId = uuid.UUID('0dfedda5-ddd3-481f-90d9-6ee388c4093e')
#     with app.app_context():
#         token = generateToken(memberId)
#         assert token is not None
    
# def testSignupWithGenerateTokenForNoneMember(app):
#     email = "jennie@gmail.com"
#     firstname = "Jennie"
#     lastname = "Kim"
#     password = "password"
#     with app.app_context():
#         member = addMember(email, firstname, lastname)
#         authMember = addOrUpdateAuth(member.memberId, password)
#         token = generateToken(authMember.memberId)
#         assert token is not None

# '''
# Route: api/login
# REST operation: PUT
# Service methods tested: getByMemberId(), generateToken()
# Cases to test:
# 1. email is not provided (catch 400 error)
# 2. password is not provided (catch 400 error)
# 5. normal case: correct info provided. check 200 response
# '''
# def testLogin(auth):
#     response = auth.login()
#     jsonResponse = json.loads(response.data.decode('utf-8'))
#     assert jsonResponse['success'] == True

# @pytest.mark.parametrize(('email', 'password', 'message'), (
# ('', 'a', 'Please provide your email.'),
# ('vitruong00@tamu.edu', '', 'Please provide a password.'),
# ('a', 'password', 'Account does not exist or incorrect. Please create an account first!'),
# ('a', 'a', 'Account does not exist or incorrect. Please create an account first!'),
# ('vitruong00@tamu.edu', 'a', 'Incorrect password!'),
# ))
# def testLoginValidateInput(auth, email, password, message):
#     response = auth.login(email, password)
#     jsonResponse = json.loads(response.data.decode('utf-8'))
#     assert message == jsonResponse['reason']
    
    
# def testLoginWithValidateMember(app, auth):
#     email = "vitruong00@tamu.edu"
#     auth.login(email)
#     with app.app_context():
#         member = getMemberByEmail(email)
#         assert member is not None

# def testLoginWithInvalidMember(app, auth):
#     email = "jennie@gmail.com"
#     auth.login(email)   
#     with app.app_context():
#         member = getMemberByEmail(email)
#         assert member is None
        
# def testLoginWithValidAuthMember(app,auth):
#     auth.login()
#     email = "vitruong00@tamu.edu"
#     with app.app_context():
#         member = getMemberByEmail(email)
#         authMember = getAuthByMemberId(member.memberId)
#         assert authMember is not None
        
# def testLoginWithNoneMember(app,auth):
#     email = "jennie@gmail.com"
#     with app.app_context():
#         member = getMemberByEmail(email)
#         if member is None:
#             response = auth.login(email)
#             jsonResponse = json.loads(response.data.decode('utf-8'))
#             assert 'Account does not exist or incorrect. Please create an account first!' == jsonResponse['reason']
            
# def testLoginWithNoneAuthMember(app,auth):
#     email = "jennie@gmail.com"
#     firstname = "Jennie"
#     lastname = "Kim"
#     with app.app_context():
#         member = addMember(email, firstname, lastname)
#         authMember = getAuthByMemberId(member.memberId)
#         if authMember is None:
#             response = auth.login(email)
#             jsonResponse = json.loads(response.data.decode('utf-8'))
#             assert 'Account does not exist or incorrect. Please create an account first!' == jsonResponse['reason']
            
# '''
# Route: api/logout
# REST operation: POST
# Service methods tested: none (just deletes cookie)
# Cases to test:
# 1. normal logout. check 200 response
# '''
# @pytest.mark.order(3)
# def testLogout(client, auth):
#     auth.login()
    
#     with client:
#         response = auth.logout()
#         jsonResponse = json.loads(response.data.decode('utf-8'))
#         assert jsonResponse == {}