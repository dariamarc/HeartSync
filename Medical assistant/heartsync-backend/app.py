import json
import logging
import os
from flask_mail import Mail
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from flask import Flask
from flask import request
from flask import make_response, jsonify
from user.user_repo import UserRepo
from flask_cors import CORS
from utils.token import confirm_token

logging.basicConfig(filename="heartsync.log")

app = Flask(__name__)
CORS(app)
env_config = os.getenv("APP_SETTINGS", "utils.config.DevelopmentConfig")
app.config.from_object(env_config)
db = create_engine('postgresql://postgres:admin@localhost/heartsync_data')
con = db.connect()
metadata = MetaData()
mail = Mail(app)
user_repo = UserRepo(con, metadata, db, app, mail)


@app.route('/', methods=['GET'])
def hello_world():
    return user_repo.get_all_users()


@app.route('/api/auth/login', methods=['POST'])
def login():
    user = json.loads(request.get_data())
    print(user)
    token = user_repo.login(user['username'], user['password'])
    if token:
        response = make_response(jsonify(accessToken=token), 200)
    else:
        response = make_response('Invalid login', 400)

    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/api/auth/signup', methods=['POST'])
def signup():
    user = json.loads(request.get_data())
    user = user_repo.signup(user['username'], user['password'], user['email'], user['firstname'], user['lastname'])
    if user:
        response = make_response(jsonify(user), 200)
    else:
        response = make_response('Username already exists', 409)

    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/api/auth/confirm', methods=['POST'])
def confirm_email():
    data = json.loads(request.get_data())
    try:
        if user_repo.confirm_email(data['token']):
            response = make_response('Email confirmed successfully', 200)
    except:
        response = make_response('The confirmation link is invalid or has expired', 409)

    response.headers['Content-Type'] = 'application/json'
    return response


if __name__ == '__main__':
    app.run()
