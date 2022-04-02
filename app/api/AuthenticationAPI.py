import os
from flask import jsonify, make_response, request, session
from flask_restful import Resource
from app.services.AuthService import *
from app.services.MemberService import *
from  werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

class AuthenticationApi(Resource):
    # log in
    def put(self):
        data = request.get_json(force=True)
        authResp = {
            'reason': ''
        }

        if not data or not data.get('email') or not data.get('password'):
            authResp['reason'] = "Please provide both an email and password!"
            return make_response(jsonify(authResp), 401)
            
        member = getByEmail(data['email'])

        if not member:
            authResp['reason'] = "Account does not exist. Please create an account first!"
            return make_response(jsonify(authResp), 403)
        
        authMember = getByMemberId(member.memberId)
        print("Authenticated member is", authMember)
        if not authMember:
            authResp['reason'] = "Account does not exist. Please create an account first!"
            return make_response(jsonify(authResp), 403)
    
        if check_password_hash(authMember.password, data['password']):
            # generates the JWT Token
            try:
                token = generateToken(authMember.memberId)
            except:
                authResp['reason'] = "Sorry, we are having some trouble logging you in at this time. Please try again later."
                return make_response(jsonify(authResp), 401)

            authResp = make_response(jsonify({'succcess' : True}))
            authResp.set_cookie('hhub-token', value=str(token))
            return authResp
        
        authResp['reason'] = "Incorrect password!"
        return make_response(jsonify(authResp), 403)
    
    # create an account
    def post(self):
        data = request.get_json(force=True)
       
        authResp = {
            'reason': ''
        }

        email = data['email']
        firstname = data['firstname']
        lastname = data['lastname']
        password = generate_password_hash(data['password'])
        member = getByEmail(email)
        
        # If you are not a member, create a new member
        if not member:
            member = addMember(email, firstname, lastname)
            
        authMember = getByMemberId(member.memberId)
        # If you are a member but not authenticated yet
        if not authMember:
            newMember = addOrUpdateAuth(member.memberId, password)
            try:
                token = generateToken(newMember.memberId)
            except:
                authResp['reason'] = "We are running into some issues, we apologize. Please try again later."
                return make_response(jsonify(authResp), 401)
            
            authResp = make_response(jsonify({'succcess' : True}))
            authResp.set_cookie('hhub-token', value=str(token))
            return authResp
        # If are an authenticated member
        else:
            try:
                token = generateToken(authMember.memberId)
            except:
                authResp['reason'] = "We are running into some issues, we apologize. Please try again later."
                return make_response(jsonify(authResp), 401)
            
            authResp = make_response(jsonify({'succcess' : True}))
            authResp.set_cookie('hhub-token', value=str(token))
            return authResp