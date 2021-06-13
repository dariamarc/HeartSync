import io
import json
import logging
import os
from gzip import GzipFile
from flask_mail import Mail
from nibabel import FileHolder, Nifti1Image
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from flask import Flask
from flask import request
from flask import make_response, jsonify
from comment.comment_repo import CommentRepo
from comment.comment_service import CommentService
from file.file_repo import FileRepo
from file.file_service import FileService
from myutils.config import DevelopmentConfig
from note.note_repo import NoteRepo
from note.note_service import NoteService
from scan.scan_repo import ScanRepo
from scan.scan_service import ScanService
from mytest.test import Test
from user.user_repo import UserRepo
from flask_cors import CORS
from user.user_service import UserService

logging.basicConfig(filename="heartsync.log")

app = Flask(__name__)
CORS(app)
env_config = DevelopmentConfig
app.config.from_object(env_config)

try:
    db = create_engine('postgresql://postgres:admin@localhost/heartsync_data')
    con = db.connect()
    metadata = MetaData()
except:
    logging.error("Failed to connect to database.")

mail = Mail(app)

user_repo = UserRepo(con, metadata, db, app, mail)
user_service = UserService(user_repo)
file_repo = FileRepo(con, metadata, db, app)
file_service = FileService(file_repo)
scan_repo = ScanRepo(con, metadata, db, app)
scan_service = ScanService(scan_repo)
notes_repo = NoteRepo(con, metadata, db, app)
notes_service = NoteService(notes_repo)
comment_repo = CommentRepo(con, metadata, db, app)
comment_service = CommentService(comment_repo)


@app.route('/api/auth/login', methods=['POST'])
def login():
    user = json.loads(request.get_data())
    if 'username' not in user.keys() or 'password' not in user.keys():
        response = make_response('Invalid login parameters', 400)
    else:
        logging.info("Logging in for user " + user['username'])
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
    if 'username' not in user.keys() or 'password' not in user.keys() or 'email' not in user.keys() or 'firstname' not in user.keys() or 'lastname' not in user.keys():
        response = make_response('Invalid signup parameters', 400)
    else:
        user = user_service.signup(user['username'], user['password'], user['email'], user['firstname'],
                                   user['lastname'])
        if user:
            response = make_response(jsonify(user), 200)
        else:
            response = make_response('Username already exists', 409)

    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/api/auth/confirm', methods=['POST'])
def confirm_email():
    data = json.loads(request.get_data())
    if not data['token']:
        response = make_response('Invalid confirm parameters', 400)
    else:
        try:
            if user_service.confirm_email(data['token']):
                response = make_response('Email confirmed successfully', 200)
        except:
            response = make_response('The confirmation link is invalid or has expired', 409)

    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/api/scans/add', methods=['POST'])
def process_file():
    if 'Authorization' not in request.headers.keys():
        response = make_response('Missing authentication token', 400)
    else:
        full_token = request.headers['Authorization']

        if full_token is None:
            response = make_response('Unauthorized action! Token is invalid', 401)

        else:
            token = full_token.strip().split(" ")[1]
            user = user_service.get_user_by_token(token)

            if user is None:
                response = make_response('Unauthorized action! Token is invalid', 401)
            else:
                if 'file' not in request.files.keys():
                    response = make_response('Invalid parameters', 400)
                else:
                    file = request.files['file']

                    if file is None:
                        response = make_response('File is missing!', 409)
                    elif file_service.check_file_type(file):
                        fh = FileHolder(fileobj=GzipFile(fileobj=io.BytesIO(file.read())))
                        img = Nifti1Image.from_file_map({'header': fh, 'image': fh})
                        file_id = file_service.segment_image(img)
                        scan_name = file.filename.split(".")[0]
                        scan = scan_service.save_scan(user.username, file_id, scan_name)
                        response = make_response(scan, 200)
                    else:
                        response = make_response('Invalid file type!', 415)

    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/api/scans/get', methods=['GET'])
def get_user_scans():
    if 'Authorization' not in request.headers.keys():
        response = make_response('Missing authentication token', 400)
    else:
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


@app.route('/api/files/get/<int:scanid>', methods=['GET'])
def get_file(scanid):
    if 'Authorization' not in request.headers.keys():
        response = make_response('Missing authentication token', 400)
    else:
        full_token = request.headers['Authorization']

        if scanid is None:
            response = make_response('Invalid parameters', 400)
        else:
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
                    fileid = scan_service.get_scan_file(scanid)
                    file_contents = file_service.get_file(fileid)
                    response = make_response(jsonify(file_contents), 200)
                    response.headers['Content-Type'] = "application/json"

    return response


@app.route('/api/notes/add/<int:scanid>', methods=['POST'])
def save_notes(scanid):
    if 'Authorization' not in request.headers.keys():
        response = make_response('Missing authentication token', 400)
    else:
        full_token = request.headers['Authorization']

        if scanid is None:
            response = make_response('Invalida parameters', 400)
        else:
            if full_token is None:
                response = make_response('Unauthorized action! Token is invalid', 401)

            else:
                token = full_token.strip().split(" ")[1]
                user = user_service.get_user_by_token(token)

                if user is None:
                    response = make_response('Unauthorized action! Token is invalid', 401)

                else:
                    data = json.loads(request.get_data())
                    note = notes_service.save_note(scanid, data['text'])
                    response = make_response(note, 200)

    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/api/notes/get/<int:scanid>', methods=['GET'])
def get_notes(scanid):
    if 'Authorization' not in request.headers.keys():
        response = make_response('Missing authentication token', 400)
    else:
        full_token = request.headers['Authorization']

        if scanid is None:
            response = make_response('Invalid parameters', 400)
        else:
            if full_token is None:
                response = make_response('Unauthorized action! Token is invalid', 401)

            else:
                token = full_token.strip().split(" ")[1]
                user = user_service.get_user_by_token(token)

                if user is None:
                    response = make_response('Unauthorized action! Token is invalid', 401)

                else:
                    note = notes_service.get_note_by_scan(scanid)
                    if note is None:
                        note = ''
                    response = make_response(note, 200)

    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/api/comments/add/<int:scanid>', methods=['POST'])
def add_comment(scanid):
    if 'Authorization' not in request.headers.keys():
        response = make_response('Missing authentication token', 400)
    else:
        full_token = request.headers['Authorization']

        if scanid is None:
            response = make_response('Invalid parameters', 400)
        else:
            if full_token is None:
                response = make_response('Unauthorized action! Token is invalid', 401)

            else:
                token = full_token.strip().split(" ")[1]
                user = user_service.get_user_by_token(token)

                if user is None:
                    response = make_response('Unauthorized action! Token is invalid', 401)

                else:
                    data = json.loads(request.get_data())
                    if 'text' not in data.keys() or data['text'] == '':
                        response = make_response('Comment cannot be empty', 400);
                    else:
                        comment = comment_service.save_comment(scanid, user.username, data['text'])
                        response = make_response(comment, 200)

    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/api/comments/get/<int:scanid>', methods=['GET'])
def get_comments(scanid):
    if 'Authorization' not in request.headers.keys():
        response = make_response('Missing authentication token', 400)
    else:
        full_token = request.headers['Authorization']

        if scanid is None:
            response = make_response('Invalid parameters', 400)
        else:
            if full_token is None:
                response = make_response('Unauthorized action! Token is invalid', 401)

            else:
                token = full_token.strip().split(" ")[1]
                user = user_service.get_user_by_token(token)

                if user is None:
                    response = make_response('Unauthorized action! Token is invalid', 401)

                else:
                    comments = comment_service.get_comments_by_scan(scanid)
                    response = make_response(comments, 200)

    response.headers['Content-Type'] = 'application/json'
    return response


if __name__ == '__main__':
    tester = Test(comment_repo, comment_service, file_repo, file_service, notes_repo, notes_service, scan_repo, scan_service)
    tester.run()
    logging.info("Tests passed")
    # app.run()
