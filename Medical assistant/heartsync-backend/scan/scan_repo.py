import json

from sqlalchemy import Table
from sqlalchemy import select

from scan.scan import Scan


class ScanRepo:
    def __init__(self, con, metadata, engine, app):
        self.con = con
        self.app = app
        self.scans = Table('scans', metadata, autoload=True, autoload_with=engine)

    def add_scan(self, username, fileid, name):
        ins = self.scans.insert().values(username=username, fileid=fileid, name=name)
        result = self.con.execute(ins)

        return result.inserted_primary_key

    def get_user_scans(self, username):
        query = select([self.scans]).where(username == username)
        result_proxy = self.con.execute(query)
        result_set = result_proxy.fetchall()
        scans = []
        for i, result in enumerate(result_set):
            scan = Scan(result[0], result[1], result[2], result[3])
            scans.append(scan.get_scan())
        return json.dumps(scans)