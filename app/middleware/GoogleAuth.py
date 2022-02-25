# External imports
import os
import pathlib
import google.auth.transport.requests
import requests
from flask import session, abort, redirect, request
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from pip._vendor import cachecontrol

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")
redirect_path = os.getenv('REDIRECT_PATH')

flow = Flow.from_client_secrets_file(client_secrets_file=client_secrets_file, 
                                     scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email","openid"],
                                     redirect_uri=redirect_path)

def createUserAccount():
    pass

def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return authorization_url

def checkLogin():
        
    #print(request.args.get('state'), session.get('state'))
    print("You need to login or create an account")
    
    if not session.get("state") == request.args.get("state"):
        return False
    return True
    
def getUserCredentials():

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
    print(id_info)
    
    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    
    # TODO: CREATE USER WITH SERVICE IF NOT EXISTS
    # IF DOES EXIST ATTACH USER_ID TO HEADER
