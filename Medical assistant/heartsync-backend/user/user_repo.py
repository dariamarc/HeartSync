from flask import jsonify, url_for, render_template
from sqlalchemy import Table
from sqlalchemy import select, update
from user.user import User
from passlib.hash import pbkdf2_sha256
from utils.email import send_email
from utils.token import encode_auth_token, generate_confirmation_token, confirm_token


class UserRepo:
    def __init__(self, con, metadata, engine, app, mail):
        self.con = con
        self.app = app
        self.mail = mail
        self.users = Table('users', metadata, autoload=True, autoload_with=engine)

    def get_all_users(self):
        query = select([self.users])
        result_proxy = self.con.execute(query)
        result_set = result_proxy.fetchall()
        users = {}
        for i, result in enumerate(result_set):
            user = User(result[0], result[1], result[2], result[3], result[4])
            users[i] = (user.get_user())
        return users

    def login(self, username, password):
        query = select(self.users).where(self.users.c.username == username)
        user = None
        for row in self.con.execute(query):
            user = User(row[0], row[1], row[2], row[3], row[4])

        if user and pbkdf2_sha256.verify(password, user.password):
            auth_token = encode_auth_token(user.username)
            update_query = update(self.users).where(self.users.c.username == username).values(token=auth_token.decode('utf-8'))
            self.con.execute(update_query)
            return auth_token
        else:
            return None

    def confirm_email(self, email_token):
        email = confirm_token(email_token, self.app)
        if not email:
            return False

        upd = update(self.users).where(self.users.c.email == email).values(confirmed=True)
        result = self.con.execute(upd)
        if result:
            return True
        return False

    def signup(self, username, password, email, firstname, lastname):

        query = select(self.users).where(self.users.c.username == username)
        result = self.con.execute(query)
        if result.fetchone():
            return None

        password = pbkdf2_sha256.hash(password)
        ins = self.users.insert().values(username=username, password=password, email=email, firstname=firstname, lastname=lastname, confirmed=False)
        result = self.con.execute(ins)

        token = generate_confirmation_token(email, self.app)
        confirm_url = "localhost:8100/confirm/" + token
        html = render_template('confirmation_email.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(email, subject, html, self.app, self.mail)

        return result.inserted_primary_key
