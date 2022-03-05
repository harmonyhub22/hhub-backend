import os
import flask
import google_auth_oauthlib
from google.oauth2 import id_token
import google.auth.transport.requests
import requests

from app.services.MemberService import addMember, getByEmail

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)

client_config = dict()
client_config['web'] = {
    'client_id': os.getenv('CLIENT_ID'),
    'project_id': os.getenv('PROJECT_ID'),
    'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
    'token_uri': 'https://oauth2.googleapis.com/token',
    'auth_provider_x509_cert_url': 'https://www.googleapis.com/oauth2/v1/certs',
    'client_secret': os.getenv('CLIENT_SECRET'),
    'redirect_uris': os.getenv('REDIRECT_URIS'),
}

def is_logged_in():
    return ('memberId' in flask.session)

def is_logging_in():
    return ('oauth' in flask.request.endpoint)

def enforce_login():
    if not is_logged_in() and not is_logging_in():
        flask.session['request_full_path'] = flask.request.full_path
        return flask.redirect(flask.url_for('oauth.index'))

def create_flow(state=None):
    flow = google_auth_oauthlib.flow.from_client_config(client_config=client_config, 
                                scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email","openid"],
                                state=state)
    flow.redirect_uri = flask.url_for('oauth.callback', _external=True)
    return flow

def get():
    flow = create_flow()
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')
    flask.session['state'] = state
    return flask.redirect(authorization_url)

def callback():
    flow = create_flow(flask.session['state'])
    flow.fetch_token(authorization_response=flask.request.url)
    flask.session['credentials'] = oauth2_credentials_to_dict(flow.credentials)
    #credentials = flow.credentials
    #request_session = requests.session()
    #cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=flask.session['credentials'])
    
    id_info = id_token.verify_oauth2_token(
        id_token=flask.session['credentials']._id_token,
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
    
    flask.session['memberid'] = member.memberId
    return flask.redirect(flask.session['request_full_path'])

def oauth2_credentials_to_dict(credentials):
    return {'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes}