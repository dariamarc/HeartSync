import json
import os
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from flask import Flask
from flask import request
from flask import make_response, jsonify
from user.user_repo import UserRepo
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)
db = create_engine('postgresql://postgres:admin@localhost/heartsync_data')
con = db.connect()
metadata = MetaData()
user_repo = UserRepo(con, metadata, db)


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


if __name__ == '__main__':
    app.run()
