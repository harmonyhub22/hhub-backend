# External imports
import os
import pathlib
import google.auth.transport.requests
import requests
from flask import session, request
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from pip._vendor import cachecontrol
from app.exceptions.UnauthorizedException import UnauthorizedException
from app.services.MemberService import getByEmail, addMember

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")
redirect_path = os.getenv('REDIRECT_PATH', 'http://localhost:5000/google-login')

flow = Flow.from_client_secrets_file(client_secrets_file=client_secrets_file, 
                                     scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email","openid"],
                                     redirect_uri=redirect_path)

def getSession():
    try:
        print(session)
        return session['memberid']
    except Exception:
        return None

def login():
    authorization_url, state = flow.authorization_url()
    session['state'] = state
    return authorization_url

def verifyLogin():
    print(request.args.get('state'), session.get('state'))
    if session['state'] != request.args.get('state'):
        raise UnauthorizedException('Google Login Failed')
    
def getOrCreateMember():

    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)
    
    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    email = id_info.get('email')
    firstname = id_info.get("given_name")
    lastname = id_info.get("family_name")
    
    member = getByEmail(email)
   
    if not member:
        member = addMember(email, firstname, lastname)
        print(member.email)
        return member.memberId
    
    session['memberid'] = member.memberId

    print(member.memberId)
    return session['memberid']
    
    
        