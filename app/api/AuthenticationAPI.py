import os
from flask import jsonify, make_response, request, session
from flask_restful import Resource
from app.middleware.NoAuth import token_required
from app.services.AuthService import *
from app.services.MemberService import *
from  werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import uuid

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
        
        password = data['password']
        if check_password_hash(data.password, password):
            # generates the JWT Token
            hashedPassword = generate_password_hash(password)
            addOrUpdateAuth(member.memberId, hashedPassword)

            try:
                token = generateToken(member.memberId)
            except:
                authResp['reason'] = "Sorry, we are having some trouble logging you in at this time. Please try again later."
                return make_response(jsonify(authResp), 401)

            secret = os.environ.get("SECRET_KEY", None)
            if secret == None:
                authResp['reason'] = "We are running into some issues, we apologize. Please try again later."
                return make_response(jsonify(authResp), 401)                
            
            token = jwt.encode({
                'memberId': str(member.memberId),
                'exp' : datetime.utcnow() + timedelta(hours=24)
            }, secret)

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
        member = getByEmail(email)

        password = generate_password_hash(member.memberId)

        if not member:
            addOrUpdateAuth(member.memberId, password)
            try:
                token = generateToken(member.memberId)
            except:
                authResp['reason'] = "We are running into some issues, we apologize. Please try again later."
                return make_response(jsonify(authResp), 401)
            
            authResp = make_response(jsonify({'succcess' : True}))
            authResp.set_cookie('hhub-token', value=str(token))
            return authResp
        else:
            return make_response('A user with this email already exists!', 202)