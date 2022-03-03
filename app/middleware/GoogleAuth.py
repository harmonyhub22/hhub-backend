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
redirect_path = str(os.getenv('SERVER_DOMAIN') + os.getenv('REDIRECT_PATH'))

client_config = dict()
client_config['web'] = {
    'client_id': os.getenv('CLIENT_ID'),
    'project_id': os.getenv('PROJECT_ID'),
    'auth_uri': os.getenv('AUTH_URI'),
    'token_uri': os.getenv('TOKEN_URI'),
    'auth_provider_x509_cert_url': os.getenv('AUTH_PROVIDER_X509_CERT_URL'),
    'client_secret': os.getenv('CLIENT_SECRET'),
    'redirect_uris': os.getenv('REDIRECT_URIS'),
}

flow = Flow.from_client_config(client_config=client_config, 
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
    print("Current member ", member)
   
    if not member:
        print("You are not in our system")
        member = addMember(email, firstname, lastname)
        return member.memberId
    
    session['memberid'] = member.memberId
    return session['memberid']
    
    
        