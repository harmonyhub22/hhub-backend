from flask import Flask
from flask import jsonify

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Welcome to the Harmony Hub Server"

@app.route("/ping", methods=['GET'])
def ping():
    return jsonify(success=True)