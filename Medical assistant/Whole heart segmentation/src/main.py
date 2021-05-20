import tensorflow

from src.model.losses import one_hot
from src.model.model import build_model, train_model, get_model
from src.data.load_data import load_training_data_ct, load_data

if __name__ == '__main__':
    train_model()
    # get_model()
    # v = [[1], [2]]
    # v = one_hot(v)
    # print(v)