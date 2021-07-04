import re


class UserService:
    def __init__(self, user_repo):
        self.user_repo = user_repo

    def login(self, username, password):
        return self.user_repo.login(username, password)

    def signup(self, username, password, email, firstname, lastname):
        id = self.user_repo.signup(username, password, email, firstname, lastname)

        return id

    def get_user_by_token(self, token):
        return self.user_repo.get_user_by_token(token)

    def validate_user(self, user):
        print(self.validate_username(user['username']))
        print(self.validate_password(user['password']))
        print(self.validate_email(user['email']))
        print(self.validate_firstname(user['firstname']))
        print(self.validate_lastname(user['lastname']))
        if self.validate_username(user['username']) and self.validate_password(user['password']) and self.validate_email(user['email']) and self.validate_firstname(user['firstname']) and self.validate_lastname(user['lastname']):
            return True
        return False

    def validate_username(self, username):
        if username == '':
            return False
        return True

    def validate_password(self, password):
        if len(password) > 5:
            return True
        elif len(password) >= 3:
            regex = "^(?=.*[a-z])(?=.*[0-9])(?=.*[.!@#$%^&*])"
            if re.match(regex, password):
                return True
            return False
        return False

    def validate_email(self, email):
        if email == '':
            return False
        if email.find('@'):
            return True
        return False

    def validate_firstname(self, firstname):
        if firstname == '':
            return False
        return True

    def validate_lastname(self, lastname):
        if lastname == '':
            return False
        return True

