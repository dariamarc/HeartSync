import io

import numpy

from heartseg.src.model.model import UnetModel


class FileService:
    def __init__(self, file_repo):
        self.file_repo = file_repo
        self.heart_segmenter = UnetModel('heartseg_model_v2.h5')

    def check_file_type(self, file):
        if file.content_type == 'application/gzip' or file.content_type == 'application/x-gzip':
            return True
        return False

    def segment_image(self, image):
        if image is not None:
            image = image.get_fdata()
            result = self.heart_segmenter.test_model(image)
            file_path, file_size = self.file_repo.save_image_file(result)
            file_type = 'obj'
            file_id = self.file_repo.add_file(file_path, file_type, file_size)
            return file_id[0]
        return None

    def get_file(self, file_id):
        file = self.file_repo.get_file(file_id)
        if file:
            path_to_file = file.file
            f = open(path_to_file, "r")
            fi = io.FileIO(f.fileno())
            breader = io.BufferedReader(fi)
            contents = breader.read()
            filename = path_to_file.split('\\')[-1]
            return {'content': contents, 'name': filename}
        return None

