import datetime
import json
import jwt
from utils.config import Config


class User:
    def __init__(self, username, password, email, firstname, lastname):
        self.__username = username
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

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                Config.SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            print(e)

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
