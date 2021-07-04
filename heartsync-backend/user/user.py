import json


class User:
    def __init__(self, username, password, email, firstname, lastname):
        self.username = username
        self.password = password
        self.email = email
        self.firstname = firstname
        self.lastname = lastname

    def get_user(self):
        data = {
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'firstname': self.firstname,
            'lastname': self.lastname
        }

        return json.dumps(data)
