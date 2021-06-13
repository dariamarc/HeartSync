from flask import render_template

from myutils.email import send_email
from myutils.token import generate_confirmation_token


class UserService:
    def __init__(self, user_repo):
        self.user_repo = user_repo

    def login(self, username, password):
        return self.user_repo.login(username, password)

    def signup(self, username, password, email, firstname, lastname):
        id = self.user_repo.signup(username, password, email, firstname, lastname)
        token = generate_confirmation_token(email, self.user_repo.app)
        confirm_url = "localhost:8100/confirm/" + token
        print(confirm_url)
        html = render_template('confirmation_email.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(email, subject, html, self.user_repo.app, self.user_repo.mail)

        return id

    def confirm_email(self, email_token):
        return self.user_repo.confirm_email(email_token)

    def get_user_by_token(self, token):
        return self.user_repo.get_user_by_token(token)