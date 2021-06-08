import logging
from src.model.model import UnetModel

if __name__ == '__main__':
    logging.basicConfig(level='DEBUG')
    model = UnetModel('heartseg_model_clahe.h5')
    model.train_model()
