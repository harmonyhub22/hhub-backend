# External imports
import os
import pathlib
import google.auth.transport.requests
import requests
from flask import Flask, session, abort, redirect, request
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from pip._vendor import cachecontrol

# Internal imports
from middleware import Test


app = Flask(__name__)
app.secret_key = "HarmonyHub"

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(client_secrets_file=client_secrets_file, 
                                     scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email","openid"]
                                     ,redirect_uri="http://127.0.0.1:5000/callback")


def login_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)
        else:
            return function()
        
    return wrapper

# middleware
app.wsgi_app = Test(app.wsgi_app)

@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)
    
    if not session["state"] == request.args["state"]:
        abort(500)
        
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
    
    return redirect("/protected_area")
        
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/")
def index():
    return "Hello World! <a href='/login'> <button> Login </button></a>"

@app.route("/protected_area")
@login_required
def protected_area():
    return "Hello World! <a href='/logout'> <button> Logout </button></a>"

#api.add_resource(login, '/login')
#api.add_resource(protected_area, '/protected_area')


if __name__ == "__main__":
    app.run(debug=True)