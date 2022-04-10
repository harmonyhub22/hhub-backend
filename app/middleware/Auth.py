from functools import wraps
import os
from flask import jsonify, make_response, request
from app.exceptions.UnauthorizedException import UnauthorizedException
import jwt

def getCookie():
    if request.path == '/api/login' or request.path == '/api/signup':
        return
    
    else:
        token = request.cookies.get('hhub-token')
        print('token', token)
        if token == None:
            raise UnauthorizedException('You are not authorized to access this page!')

        secret = os.environ.get("SECRET_KEY", None)
        authResp = {}
        if secret == None:
            authResp['reason'] = "We are running into some issues, we apologize. Please try again later."
            return make_response(jsonify(authResp), 401) 
        
        try:
            data = jwt.decode(token, secret)
            print(data)
            memberId = data['memberId']
            if memberId == None or len(memberId) < 36:
                raise UnauthorizedException('no memberId cookie found')
            request.environ['HTTP_MEMBERID'] = memberId
        except:
            raise UnauthorizedException('you login has expired')
