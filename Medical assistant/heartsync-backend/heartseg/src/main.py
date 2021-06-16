import logging
from heartseg.src.model.model import UnetModel

if __name__ == '__main__':
    logging.basicConfig(level='DEBUG')
    model = UnetModel('heartsegmodel_lucky.h5', mode='train')
    model.train_model()
