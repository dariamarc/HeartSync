import json
from sqlalchemy import Table, delete
from sqlalchemy import select
from scan.scan import Scan


class ScanRepo:
    def __init__(self, con, metadata, engine, app):
        self.con = con
        self.app = app
        self.scans = Table('scans', metadata, autoload=True, autoload_with=engine)

    def insert_scan(self, username, fileid, name):
        """
        Insert scan in database
        :param username: username
        :param fileid: id of file
        :param name: name of scan
        :return:
        """
        ins = self.scans.insert().values(username=username, fileid=fileid, name=name)
        result = self.con.execute(ins)

        return result.inserted_primary_key

    def get_scan(self, id):
        """
        Get scan by id
        :param id: id of scan
        :return:
        """
        query = select([self.scans]).where(self.scans.c.id == id)
        scan = None
        for row in self.con.execute(query):
            scan = Scan(row[0], row[1], row[2], row[3])

        return scan

    def get_user_scans(self, username):
        """
        Get list of scans corresponding to the username
        :param username: username
        :return:
        """
        query = select([self.scans]).where(self.scans.c.username == username)
        result_proxy = self.con.execute(query)
        result_set = result_proxy.fetchall()
        scans = []
        for i, result in enumerate(result_set):
            scan = Scan(result[0], result[1], result[2], result[3])
            scans.append(scan.get_data())
        return json.dumps(scans)

    def delete_scan(self, id):
        """
        Deletes scan with id
        :param id: id of scan
        :return:
        """
        deldb = delete(self.scans).where(self.scans.c.id == id)
        self.con.execute(deldb)
