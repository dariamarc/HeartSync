import os
from datetime import datetime
from sqlalchemy import Table, select
from file.file import File
from heartseg.src.data.utils_data import numpy_to_obj


class FileRepo:
    def __init__(self, con, metadata, engine, app):
        self.con = con
        self.app = app
        self.files = Table('files', metadata, autoload=True, autoload_with=engine)

    def add_file(self, file_path, file_type, file_size):
        ins = self.files.insert().values(type=file_type, size=file_size, filepath=file_path)
        result = self.con.execute(ins)

        return result.inserted_primary_key

    def save_image_file(self, image):
        verts, faces, normals, values = numpy_to_obj(image)

        now = datetime.now()
        dt_string = now.strftime("%d-%m-%Y-%H%M%S")

        filename = dt_string + '.obj'
        path = os.path.join('file\\files\\', filename)
        obj_file = open(path, 'w')
        for item in verts:
            obj_file.write("v {0} {1} {2}\n".format(item[0], item[1], item[2]))

        for item in normals:
            obj_file.write("vn {0} {1} {2}\n".format(item[0], item[1], item[2]))

        for item in faces:
            obj_file.write("f {0}//{0} {1}//{1} {2}//{2}\n".format(item[0], item[1], item[2]))

        obj_file.close()

        return path, os.path.getsize(path)

    def get_file(self, file_id):
        query = select(self.files).where(self.files.c.id == file_id)
        file = None
        for row in self.con.execute(query):
            file = File(row[0], row[1], row[2], row[3])

        return file

