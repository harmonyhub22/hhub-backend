import os
from flask import jsonify, make_response, request, session
from flask_restful import Resource
from app.middleware.NoAuth import token_required
from app.services.UserService import *
from  werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import jwt
import uuid

class AuthenticationApi(Resource):
    @token_required
    def get(self):
        users = getAll()
        output = []
        for user in users:
            output.append({
                'userName' : user.userName,
                'password' : user.password
            })
        return jsonify({'users': output})
    
    def put(self):
        auth = request.form

        if not auth or not auth.get('userName') or not auth.get('password'):
            # returns 401 if any password is missing
            return make_response(
                'Could not verify',
                401,
                {'WWW-Authenticate' : 'Basic realm ="Login required !!"'}
            )
        user = getUserName(auth.get('userName'))
        if not user:
            # returns 401 if user does not exist
            return make_response(
                'Could not verify',
                401,
                {'WWW-Authenticate' : 'Basic realm ="User does not exist !!"'}
            )
        if check_password_hash(user.password, auth.get('password')):
            # generates the JWT Token
            print("IDDDD", user.userID)
            token = jwt.encode({
                'userID': str(user.userID),
                'exp' : datetime.utcnow() + timedelta(minutes = 30)
            }, os.environ.get("SECRET_KEY", None))
            print("The token is", token)
            return make_response(jsonify({'token' : token}), 201)
        
        # returns 403 if password is wrong
        return make_response(
            'Could not verify',
            403,
            {'WWW-Authenticate' : 'Basic realm ="Wrong Password !!"'}
        )
        
    def post(self):
        # creates a dictionary of the form data
        data = request.form

        userName = data.get('userName')
        password = generate_password_hash(data.get('password'))
        
        # checking for existing user
        user = getUserName(userName)
        if not user:
            user = addUser(userName, password)
            return make_response('Successfully registered.', 201)
        else:
            # returns 202 if user already exists
            return make_response('User already exists. Please Log in.', 202)