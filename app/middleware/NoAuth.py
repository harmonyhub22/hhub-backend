from functools import wraps
import os
from flask import jsonify, request
from app.exceptions.UnauthorizedException import UnauthorizedException
import jwt
from app.services.UserService import *


def getCookie():
    memberId = request.cookies.get('memberId')
    print(request.path)
    if request.path == '/api/login':
        if memberId != None:
            request.environ['HTTP_MEMBERID'] = memberId
        return
    if memberId == None or len(memberId) < 36:
        raise UnauthorizedException('no memberId cookie found')
    request.environ['HTTP_MEMBERID'] = memberId

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
            print("The Token is", token)
            
        # return 401 if token is not passed
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401
  
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, os.environ.get("SECRET_KEY", None))
            print("The data is", data)
            current_user = getUserID(data['userID'])
            print("Current user is", current_user)
        except:
            return jsonify({
                'message' : 'Token is invalid !!'
            }), 401
        # returns the current logged in users contex to the routes
        return  f(current_user, *args, **kwargs)
  
    return decorated