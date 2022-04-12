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
            'reason': '',
            'success': False,
            'hhub-token': '',
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

            print('setting cookie to', token)
            authResp['hhub-token'] = token
            authResp['success'] = True
            resp = make_response(jsonify(authResp))
            try:
                print('cookie domain', os.getenv('COOKIE_DOMAIN'))
                resp.set_cookie(
                    key='hhub-token',
                    value=str(token),
                    secure=True,
                    max_age=timedelta(days=1), 
                    path="/",
                    samesite='None',
                    domain=os.getenv('COOKIE_DOMAIN')
                )
                #resp.headers["Set-Cookie"] = "hhub-token=" + str(token)
            except Exception as exc:
                print(str(exc))
                print('setting normal cookie')
                resp.set_cookie(key='hhub-token', value=str(token))
            return resp
        else:
            print('incorrect password')
            authResp['reason'] = "Incorrect password!"
            return make_response(jsonify(authResp), 403)
    
    # sign up
    def post(self):
        data = request.get_json(force=True)
       
        authResp = {
            'reason': '',
            'success': False,
            'hhub-token': ''
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

        if authMember != None:
            authResp['reason'] = "Member with this password already exists"
            return make_response(jsonify(authResp), 401)
        
        newMember = addOrUpdateAuth(member.memberId, password)
        try:
            token = generateToken(newMember.memberId)
        except:
            authResp['reason'] = "We are running into some issues, we apologize. Please try again later."
            return make_response(jsonify(authResp), 401)
        
        authResp['success'] = True
        authResp['hhub-token'] = str(token)
        resp = make_response(jsonify(authResp))
        try:
            resp.set_cookie('hhub-token', value=str(token), domain=os.getenv('COOKIE_DOMAIN'))
        except Exception:
            resp.set_cookie('hhub-token', value=str(token))
        return resp