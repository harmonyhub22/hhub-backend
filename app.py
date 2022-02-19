from flask import Flask
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)

app.config.from_object(os.getenv('APP_SETTINGS', 'config.DevelopmentConfig'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db) # this

@app.route("/")
def hello_world():
    return "Welcome to the Harmony Hub Server"

@app.route("/ping", methods=['GET'])
def ping():
    return jsonify(success=True)

if __name__ == '__main__':
    app.run()