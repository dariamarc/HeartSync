import base64
import io
import os
from datetime import datetime
from heartseg.src.data.utils_data import numpy_to_obj
from heartseg.src.model.model import UnetModel


class FileService:
    def __init__(self, file_repo):
        self.file_repo = file_repo
        self.heart_segmenter = UnetModel('heartsegmodel_lucky.h5', mode='test')

    def check_file_type(self, file):
        """
        Check type of file to be gzip or x-gzip
        :param file: file to be checked
        :return:
        """
        if file.content_type == 'application/gzip' or file.content_type == 'application/x-gzip':
            return True
        return False

    def process_file(self, image):
        """
        Get the image segmentation result
        :param image: image to be segmented
        :return: id of inserted result file
        """
        if image is not None:
            image = image.get_fdata()
            result = self.heart_segmenter.process_image(image)
            file_path, file_size = self.save_image_file(result)
            file_type = 'obj'
            file_id = self.file_repo.insert_file(file_path, file_type, file_size)
            return file_id[0]
        return None

    def save_image_file(self, image):
        """
        Save prediction results in obj format
        :param image: prediction result
        :return: path of saved file and size
        """
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
        """
        Get file by file id
        :param file_id: id of file
        :return: file content and filename
        """
        file = self.file_repo.get_file(file_id)
        if file:
            path_to_file = file.file
            f = open(path_to_file, "r")
            fi = io.FileIO(f.fileno())
            breader = io.BufferedReader(fi)
            contents = breader.read()
            filename = path_to_file.split('\\')[-1]
            return {'content': base64.b64encode(contents), 'name': filename}
        return None

