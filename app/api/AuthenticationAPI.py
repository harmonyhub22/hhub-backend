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

        if not data:
            authResp['reason'] = "Please provide your information."
            return make_response(jsonify(authResp), 400)
        elif not data.get('email'):
            authResp['reason'] = "Please provide your email."
            return make_response(jsonify(authResp), 400)
        elif not data.get('password'):
            authResp['reason'] = "Please provide a password."
            return make_response(jsonify(authResp), 400)
            
        member = getMemberByEmail(data.get('email'))

        if not member:
            authResp['reason'] = "Account does not exist! Please create an account first, or check that you entered the correct information!"
            return make_response(jsonify(authResp), 400)
        
        authMember = getAuthByMemberId(member.memberId)
        if not authMember:
            authResp['reason'] = "There was a problem logging you in. We are sorry about that! Please try again later."
            return make_response(jsonify(authResp), 400)
    
        if check_password_hash(authMember.password, data['password']):
            try:
                token = generateToken(authMember.memberId)
            except:
                authResp['reason'] = "There was a problem logging you in. We are sorry about that! Please try again later."
                return make_response(jsonify(authResp), 401)

            authResp = make_response(jsonify({'success' : True}))
            authResp.set_cookie('hhub-token', value=str(token))
            return authResp
        else:
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