import os
from datetime import datetime
from sqlalchemy import Table, select, delete
from file.file import File
from heartseg.src.data.utils_data import numpy_to_obj


class FileRepo:
    def __init__(self, con, metadata, engine, app):
        self.con = con
        self.app = app
        self.files = Table('files', metadata, autoload=True, autoload_with=engine)

    def insert_file(self, file_path, file_type, file_size):
        """
        Insert file into database
        :param file_path: path of the file
        :param file_type: type of file
        :param file_size: size of file
        :return: primary key of inserted file
        """
        ins = self.files.insert().values(type=file_type, size=file_size, filepath=file_path)
        result = self.con.execute(ins)

        return result.inserted_primary_key

    def get_file(self, file_id):
        """
        Get file by id
        :param file_id: id of file
        :return: file with id
        """
        query = select(self.files).where(self.files.c.id == file_id)
        file = None
        for row in self.con.execute(query):
            file = File(row[0], row[1], row[2], row[3])

        return file

    def delete_file(self, id):
        """
        Deletes file with id
        :param id: id of file
        :return:
        """
        deldb = delete(self.files).where(self.files.c.id == id)
        self.con.execute(deldb)

