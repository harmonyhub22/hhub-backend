import os
from flask import jsonify, make_response, request, session
from flask_restful import Resource
from app.services.AuthService import getByMemberId as getAuthByMemberId
from app.services.AuthService import generateToken, addOrUpdateAuth
from app.services.MemberService import getByEmail as getMemberByEmail
from app.services.MemberService import addMember
from  werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

class AuthenticationApi(Resource):

    # log in
    def put(self):
        data = request.get_json(force=True)
        authResp = {
            'reason': ''
        }
        print(data)

        if not data:
            authResp['reason'] = "Please provide your information."
            return make_response(jsonify(authResp), 400)
        elif not data.get('email'):
            print('no email')
            authResp['reason'] = "Please provide your email."
            return make_response(jsonify(authResp), 400)
        elif not data.get('password'):
            print('no password')
            authResp['reason'] = "Please provide a password."
            return make_response(jsonify(authResp), 400)
            
        member = getMemberByEmail(data.get('email'))

        if not member:
            print('no member found')
            authResp['reason'] = "Account does not exist or incorrect. Please create an account first!"
            return make_response(jsonify(authResp), 400)
        
        authMember = getAuthByMemberId(member.memberId)
        if not authMember:
            print('no auth')
            authResp['reason'] = "Account does not exist or incorrect. Please create an account first!"
            return make_response(jsonify(authResp), 400)
    
        if check_password_hash(authMember.password, data['password']):
            token = ''
            try:
                token = generateToken(authMember.memberId)
            except:
                print('could not generate token')
                authResp['reason'] = "Sorry, we are having some trouble logging you in at this time. Please try again later."
                return make_response(jsonify(authResp), 401)

            print('setting cookie')
            authResp = make_response(jsonify({'success' : True}))
            try:
                print('domain set', os.getenv('COOKIE_DOMAIN'))
                authResp.set_cookie(key='hhub-token', value=str(token), domain=os.getenv('COOKIE_DOMAIN'),
                    secure=True, path="/", httponly=False, expires=datetime.utcnow()+timedelta(minutes=1440), 
                    samesite=None)
            except:
                print('no domain set')
                authResp.set_cookie('hhub-token', value=str(token))
            return authResp
        else:
            print('incorrect password')
            authResp['reason'] = "Incorrect password!"
            return make_response(jsonify(authResp), 403)
    
    # sign up
    def post(self):
        data = request.get_json(force=True)
       
        authResp = {
            'reason': ''
        }

        if not data:
            authResp['reason'] = "Please provide your information."
            return make_response(jsonify(authResp), 400)
        elif not data.get('email'):
            authResp['reason'] = "Please provide your email."
            return make_response(jsonify(authResp), 400)
        elif not data.get('password'):
            authResp['reason'] = "Please provide a password."
            return make_response(jsonify(authResp), 400)
        elif not data.get('lastname') or not data.get('firstname'):
            authResp['reason'] = "Please provide your first and last name."
            return make_response(jsonify(authResp), 400)

        email = data['email']
        firstname = data['firstname']
        lastname = data['lastname']
        password = generate_password_hash(data['password'])
        member = getMemberByEmail(email)
        
        # If you are not a member, create a new member
        if not member:
            member = addMember(email, firstname, lastname)
        else:
            authResp['reason'] = "Member with this email already exists."
            return make_response(jsonify(authResp), 400)
            
        authMember = getAuthByMemberId(member.memberId)

        # If you are a member but not authenticated yet
        if not authMember:
            newMember = addOrUpdateAuth(member.memberId, password)
            try:
                token = generateToken(newMember.memberId)
            except:
                authResp['reason'] = "We are running into some issues, we apologize. Please try again later."
                return make_response(jsonify(authResp), 401)
            
            authResp = make_response(jsonify({'success' : True, 'reason': 'Account is already registered.'}))
            authResp.set_cookie('hhub-token', value=str(token))
            return authResp

        # If are an authenticated member
        else:
            try:
                token = generateToken(authMember.memberId)
            except:
                authResp['reason'] = "We are running into some issues, we apologize. Please try again later."
                return make_response(jsonify(authResp), 401)
            
            authResp = make_response(jsonify({'success' : True, 'reason': 'Account is already registered.'}))
            authResp.set_cookie('hhub-token', value=str(token))
            return authResp