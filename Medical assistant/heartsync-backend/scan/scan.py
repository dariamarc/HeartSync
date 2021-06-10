import json


class Scan:
    def __init__(self, id, username, fileid, name):
        self.id = id
        self.username = username
        self.fileid = fileid
        self.name = name

    def get_scan(self):
        data = {
            'id': self.id,
            'username': self.username,
            'fileid': self.fileid,
            'name': self.name
        }

        return data