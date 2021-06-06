import json


class User:
    def __init__(self, username, password, email, firstname, lastname, confirmed):
        self.username = username
        self.password = password
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.confirmed = confirmed

    def get_user(self):
        data = {
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'confirmed': self.confirmed
        }

        return json.dumps(data)
