import io
import json
import logging
import os
from gzip import GzipFile
import nibabel as nib
from flask_mail import Mail
from nibabel import FileHolder, Nifti1Image
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from flask import Flask, send_from_directory, abort
from flask import request
from flask import make_response, jsonify

from file.file_repo import FileRepo
from file.file_service import FileService
from scan.scan_repo import ScanRepo
from scan.scan_service import ScanService
from user.user_repo import UserRepo
from flask_cors import CORS

from user.user_service import UserService

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
user_service = UserService(user_repo)
file_repo = FileRepo(con, metadata, db, app)
file_service = FileService(file_repo)
scan_repo = ScanRepo(con, metadata, db, app)
scan_service = ScanService(scan_repo)

@app.route('/', methods=['GET'])
def hello_world():
    return user_repo.get_all_users()


@app.route('/api/auth/login', methods=['POST'])
def login():
    user = json.loads(request.get_data())
    print(user)
    token = user_service.login(user['username'], user['password'])
    if token:
        response = make_response(jsonify(accessToken=token), 200)
    else:
        response = make_response('Invalid login', 400)

    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/api/auth/signup', methods=['POST'])
def signup():
    user = json.loads(request.get_data())
    user = user_service.signup(user['username'], user['password'], user['email'], user['firstname'], user['lastname'])
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
        if user_service.confirm_email(data['token']):
            response = make_response('Email confirmed successfully', 200)
    except:
        response = make_response('The confirmation link is invalid or has expired', 409)

    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/api/scans/add', methods=['POST'])
def process_file():
    full_token = request.headers['Authorization']

    if full_token is None:
        response = make_response('Unauthorized action! Token is invalid', 401)

    else:
        token = full_token.strip().split(" ")[1]
        user = user_service.get_user_by_token(token)

        if user is None:
            response = make_response('Unauthorized action! Token is invalid', 401)
        else:
            file = request.files['file']
            print(file.content_type)

            if file is None:
                response = make_response('File is missing!', 409)
            elif file_service.check_file_type(file):
                fh = FileHolder(fileobj=GzipFile(fileobj=io.BytesIO(file.read())))
                img = Nifti1Image.from_file_map({'header': fh, 'image': fh})
                file_id = file_service.segment_image(img)
                scan_name = file.filename.split(".")[0]
                scan = scan_service.add_scan(user.username, file_id, scan_name)
                response = make_response(scan, 200)
            else:
                response = make_response('Invalid file type!', 415)

    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/api/scans/get', methods=['GET'])
def get_user_scans():
    full_token = request.headers['Authorization']

    if full_token is None:
        response = make_response('Unauthorized action! Token is invalid', 401)

    else:
        token = full_token.strip().split(" ")[1]
        user = user_service.get_user_by_token(token)

        if user is None:
            response = make_response('Unauthorized action! Token is invalid', 401)

        else:
            scans = scan_service.get_user_scans(user.username)
            response = make_response(scans, 200)

    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/api/files/get/<int:fileid>', methods=['GET'])
def get_file(fileid):
    full_token = request.headers['Authorization']

    if full_token is None:
        response = make_response('Unauthorized action! Token is invalid', 401)
        response.headers['Content-Type'] = 'application/json'

    else:
        token = full_token.strip().split(" ")[1]
        user = user_service.get_user_by_token(token)

        if user is None:
            response = make_response('Unauthorized action! Token is invalid', 401)
            response.headers['Content-Type'] = 'application/json'

        else:
            print(fileid)
            file_contents = file_service.get_file(fileid)
            # try:
            # return send_from_directory(app.config['SCAN_FILES'], filename)
            response = make_response(file_contents, 200);
            response.headers['Content-Type'] = "arraybuffer";
            # except:
            #     abort(404)

    return response


if __name__ == '__main__':
    app.run()
