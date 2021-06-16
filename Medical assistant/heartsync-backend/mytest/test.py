import os
import tempfile
import unittest
import flask
from flask import Flask
from flask_mail import Mail
from sqlalchemy import create_engine, MetaData

from comment.comment_repo import CommentRepo
from comment.comment_service import CommentService
from file.file_repo import FileRepo
from file.file_service import FileService
from myutils.config import DevelopmentConfig
from note.note_repo import NoteRepo
from note.note_service import NoteService
from scan.scan_repo import ScanRepo
from scan.scan_service import ScanService
from user.user_repo import UserRepo
from user.user_service import UserService


class Test():

    def set_up(self):
        app = Flask(__name__)
        env_config = DevelopmentConfig
        app.config.from_object(env_config)

        db = create_engine('postgresql://postgres:admin@localhost/heartsync')
        con = db.connect()
        metadata = MetaData()
        mail = Mail(app)

        self.user_repo = UserRepo(con, metadata, db, app, mail)
        self.user_service = UserService(self.user_repo)
        self.file_repo = FileRepo(con, metadata, db, app)
        self.file_service = FileService(self.file_repo)
        self.scan_repo = ScanRepo(con, metadata, db, app)
        self.scan_service = ScanService(self.scan_repo)
        self.notes_repo = NoteRepo(con, metadata, db, app)
        self.notes_service = NoteService(self.notes_repo)
        self.comment_repo = CommentRepo(con, metadata, db, app)
        self.comment_service = CommentService(self.comment_repo)

    def tear_down(self):
        self.scan_repo.delete_scan(self.scanid)
        self.file_repo.delete_file(self.fileid)

    def comment_repo_test(self):
        username = 'dariamarc'
        text = 'mytest'
        date = '13/05/1999'
        id = self.comment_repo.insert_comment(self.scanid, username, text, date)
        assert(self.comment_repo.get_comment_by_id(id) is not None)
        assert(self.comment_repo.get_comments_by_scan(self.scanid) != "")
        self.comment_repo.delete_comment(id[0])

    def comment_service_test(self):
        username = 'dariamarc'
        text = 'mytest'
        comment = self.comment_service.save_comment(self.scanid, username, text)
        assert(comment['scanid'] == self.scanid)
        assert(comment['username'] == 'dariamarc')
        assert(comment['text'] == 'mytest')
        assert(self.comment_service.get_comments_by_scan(self.scanid) != "")
        self.comment_repo.delete_comment(comment['id'])

    def file_repo_test(self):
        file_path = "test/path"
        file_type = "obj"
        file_size = 13
        id = self.file_repo.insert_file(file_path, file_type, file_size)
        assert(self.file_repo.get_file(id[0]) is not None)
        self.file_repo.delete_file(id[0])

    def file_service_test(self):
        file_path = "../mytest/testfile/test.txt"
        file_type = "obj"
        file_size = 13
        id = self.file_repo.insert_file(file_path, file_type, file_size)
        assert (self.file_service.get_file(id[0]) is not None)
        self.fileid = id[0]

    def note_repo_test(self):
        text = 'mytest'
        id = self.notes_repo.insert_note(self.scanid, text)
        assert (self.notes_repo.get_note_by_id(id[0]) is not None)
        assert (self.notes_repo.get_note_by_scan(self.scanid) is not None)
        self.notes_repo.delete_note(id[0])

    def note_service_test(self):
        text = 'mytest'
        note = self.notes_service.save_note(self.scanid, text)
        assert (self.notes_repo.get_note_by_id(note['id']) is not None)
        assert (self.notes_service.get_note_by_scan(self.scanid) is not None)
        self.notes_repo.delete_note(note['id'])

    def scan_repo_test(self):
        username = 'dariamarc'
        name = 'testscan'
        id = self.scan_repo.insert_scan(username, self.fileid, name)
        assert(self.scan_repo.get_scan(id[0]) is not None)
        assert(self.scan_repo.get_user_scans(username) != "")
        self.scan_repo.delete_scan(id[0])

    def scan_service_test(self):
        username = 'dariamarc'
        name = 'testscan'
        scan = self.scan_service.save_scan(username, self.fileid, name)
        assert (self.scan_service.get_scan_by_id(scan['id']) is not None)
        assert (self.scan_service.get_user_scans(username) != "")
        self.scanid = scan['id']

    def user_repo_test(self):
        username = 'test'
        password = 'test'
        firstname = 'test'
        lastname = 'test'
        email = 'test'
        self.user_repo.signup(username, password, email, firstname, lastname)
        token = self.user_repo.login(username, password)
        assert(token is not None)
        self.user_repo.delete_user(username)

    def user_service_test(self):
        username = 'test'
        password = 'test'
        firstname = 'test'
        lastname = 'test'
        email = 'test'
        self.user_repo.signup(username, password, email, firstname, lastname)
        token = self.user_service.login(username, password)
        assert (token is not None)
        self.user_repo.delete_user(username)


if __name__ == '__main__':
    test = Test()
    test.set_up()
    test.user_repo_test()
    test.user_service_test()

    test.file_repo_test()
    test.file_service_test()

    test.scan_repo_test()
    test.scan_service_test()

    test.comment_repo_test()
    test.comment_service_test()

    test.note_repo_test()
    test.note_service_test()

    test.tear_down()
    print("All tests passed successfully!")
