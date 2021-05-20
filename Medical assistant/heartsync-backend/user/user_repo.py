import json

from flask import jsonify
from sqlalchemy import Table
from sqlalchemy import select, update
from user.user import User

class UserRepo:
    def __init__(self, con, metadata, engine):
        self.con = con
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

        if password == user.password:
            auth_token = user.encode_auth_token(user.username)
            update_query = update(self.users).where(self.users.c.username == username).values(token=auth_token.decode('utf-8'))
            self.con.execute(update_query)
            return auth_token
        else:
            return None

    def signup(self, username, password, email, firstname, lastname):

        query = select(self.users).where(self.users.c.username == username)
        result = self.con.execute(query)
        if result.fetchone():
            return None

        ins = self.users.insert().values(username=username, password=password, email=email, firstname=firstname, lastname=lastname)
        result = self.con.execute(ins)

        return result.inserted_primary_key
