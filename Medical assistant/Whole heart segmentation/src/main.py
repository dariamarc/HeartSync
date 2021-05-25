import logging
from src.model.model import UnetModel

if __name__ == '__main__':
    logging.basicConfig(level='DEBUG')
    # tfc.run(stream_logs=True, docker_image_bucket_name="heartsync_data")
    model = UnetModel()
    model.train_model()
