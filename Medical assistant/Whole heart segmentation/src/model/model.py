import configparser
from random import random
import numpy as np
import tensorflow.keras.layers
from skimage.transform import resize
from sklearn.model_selection import KFold
import keras.models
import logging
import tensorflow as tf
from tensorflow import keras as k
from src.data.load_data import DataLoader
from src.data.transform_data import preprocess_data, rotate_image, rotate_tf, rotate_images, prepare_test_image
from src.model.losses import loss_fn, dice_coef
from src.utils.exception import PreprocessException
from src.data.utils_data import decompose_data_to_cubes, compose_cubes_to_vol


def conv3D(input, output, kernel_size, strides):
    """
    Builds a 3D Conv Keras layer with custom initializer
    :param input: input layer of this layer
    :param output: size of the output of this layer
    :param kernel_size: kernel size of layer
    :param strides: strides of layer
    :return: conv3d layer
    """
    return k.layers.Conv3D(filters=output, kernel_size=kernel_size, strides=strides, padding="same",
                           data_format="channels_last",
                           kernel_initializer=tf.keras.initializers.TruncatedNormal(mean=0.0, stddev=0.01),
                           kernel_regularizer=tf.keras.regularizers.l2(0.0005),
                           use_bias=False)(input)


def deconv3D(input, output):
    """
    Builds a 3D Transpose Keras layer with custom regularizer
    :param input: input layer of this layer
    :param output: output size of layer
    :return: transpose3d layer
    """
    return k.layers.Conv3DTranspose(filters=output, kernel_size=4, padding="same", strides=[2, 2, 2],
                                    kernel_regularizer=tf.keras.regularizers.l2(0.0005))(input)


class UnetModel:

    def __init__(self, model_name):
        config = configparser.ConfigParser()
        config.read('../model/init/model.ini')
        input_size = int(config.get('MODEL_INIT', 'INPUT_SIZE'))
        input_chn = int(config.get('MODEL_INIT', 'INPUT_CHANNEL'))
        self.input_shape = (input_size, input_size, input_size, input_chn)
        self.data_loader = DataLoader()
        self.model_path = config.get('MODEL_INIT', 'MODEL_DIR')
        self.model_name = model_name

    def build_model(self):
        """
        Builds U-net model for segmentation task
        :return: keras model
        """

        input = k.layers.Input(shape=self.input_shape)

        conv1 = conv3D(input=input, output=64, kernel_size=3, strides=1)
        conv1_bn = k.layers.BatchNormalization(epsilon=1e-5, scale=True, momentum=0.9)(conv1)
        conv1_relu = k.layers.ReLU()(conv1_bn)
        pool1 = k.layers.MaxPool3D(pool_size=2, strides=2)(conv1_relu)

        conv2 = conv3D(input=pool1, output=128, kernel_size=3, strides=1)
        conv2_bn = k.layers.BatchNormalization(epsilon=1e-5, scale=True, momentum=0.9)(conv2)
        conv2_relu = k.layers.ReLU()(conv2_bn)
        pool2 = k.layers.MaxPool3D(pool_size=2, strides=2)(conv2_relu)

        conv3 = conv3D(input=pool2, output=256, kernel_size=3, strides=1)
        conv3_bn = k.layers.BatchNormalization(epsilon=1e-5, scale=True, momentum=0.9)(conv3)
        conv3_relu = k.layers.ReLU()(conv3_bn)
        conv3_2 = conv3D(input=conv3_relu, output=256, kernel_size=3, strides=1)
        conv3_bn_2 = k.layers.BatchNormalization(epsilon=1e-5, scale=True, momentum=0.9)(conv3_2)
        conv3_relu_2 = k.layers.ReLU()(conv3_bn_2)
        pool3 = k.layers.MaxPool3D(pool_size=2, strides=2)(conv3_relu_2)

        conv4 = conv3D(input=pool3, output=512, kernel_size=3, strides=1)
        conv4_bn = k.layers.BatchNormalization(epsilon=1e-5, scale=True, momentum=0.9)(conv4)
        conv4_relu = k.layers.ReLU()(conv4_bn)
        conv4_2 = conv3D(input=conv4_relu, output=512, kernel_size=3, strides=1)
        conv4_bn_2 = k.layers.BatchNormalization(epsilon=1e-5, scale=True, momentum=0.9)(conv4_2)
        conv4_relu_2 = k.layers.ReLU()(conv4_bn_2)
        pool4 = k.layers.MaxPool3D(pool_size=2, strides=2)(conv4_relu_2)

        conv5 = conv3D(input=pool4, output=512, kernel_size=3, strides=1)
        conv5_bn = k.layers.BatchNormalization(epsilon=1e-5, scale=True, momentum=0.9)(conv5)
        conv5_relu = k.layers.ReLU()(conv5_bn)
        conv5_2 = conv3D(input=conv5_relu, output=512, kernel_size=3, strides=1)
        conv5_bn_2 = k.layers.BatchNormalization(epsilon=1e-5, scale=True, momentum=0.9)(conv5_2)
        conv5_relu_2 = k.layers.ReLU()(conv5_bn_2)

        deconv1 = deconv3D(input=conv5_relu_2, output=512)
        deconv1_bn = k.layers.BatchNormalization(epsilon=1e-5, scale=True, momentum=0.9)(deconv1)
        deconv1_relu = k.layers.ReLU()(deconv1_bn)

        concat1 = tensorflow.keras.layers.Concatenate(axis=4)([deconv1_relu, conv4_2])
        deconv1_2 = conv3D(input=concat1, output=256, kernel_size=3, strides=1)
        deconv1_bn_2 = k.layers.BatchNormalization(epsilon=1e-5, scale=True, momentum=0.9)(deconv1_2)
        deconv1_relu_2 = k.layers.ReLU()(deconv1_bn_2)

        deconv2 = deconv3D(input=deconv1_relu_2, output=256)
        deconv2_bn = k.layers.BatchNormalization(epsilon=1e-5, scale=True, momentum=0.9)(deconv2)
        deconv2_relu = k.layers.ReLU()(deconv2_bn)

        concat2 = tensorflow.keras.layers.Concatenate(axis=4)([deconv2_relu, conv3])
        deconv2_2 = conv3D(input=concat2, output=128, kernel_size=3, strides=1)
        deconv2_bn_2 = k.layers.BatchNormalization(epsilon=1e-5, scale=True, momentum=0.9)(deconv2_2)
        deconv2_relu_2 = k.layers.ReLU()(deconv2_bn_2)

        deconv3 = deconv3D(input=deconv2_relu_2, output=128)
        deconv3_bn = k.layers.BatchNormalization(epsilon=1e-5, scale=True, momentum=0.9)(deconv3)
        deconv3_relu = k.layers.ReLU()(deconv3_bn)

        concat3 = tensorflow.keras.layers.Concatenate(axis=4)([deconv3_relu, conv2])
        deconv3_2 = conv3D(input=concat3, output=64, kernel_size=3, strides=1)
        deconv3_bn_2 = k.layers.BatchNormalization(epsilon=1e-5, scale=True, momentum=0.9)(deconv3_2)
        deconv3_relu_2 = k.layers.ReLU()(deconv3_bn_2)

        deconv4 = deconv3D(input=deconv3_relu_2, output=64)
        deconv4_bn = k.layers.BatchNormalization(epsilon=1e-5, scale=True, momentum=0.9)(deconv4)
        deconv4_relu = k.layers.ReLU()(deconv4_bn)

        concat4 = tensorflow.keras.layers.Concatenate(axis=4)([deconv4_relu, conv1])
        deconv4_2 = conv3D(input=concat4, output=32, kernel_size=3, strides=1)
        deconv4_bn_2 = k.layers.BatchNormalization(epsilon=1e-5, scale=True, momentum=0.9)(deconv4_2)
        deconv4_relu_2 = k.layers.ReLU()(deconv4_bn_2)

        output = k.layers.Conv3D(8, kernel_size=1, strides=1)(deconv4_relu_2)
        prob = k.layers.Softmax()(output)

        model = k.models.Model(inputs=input, outputs=prob)

        print(model.summary())

        return model


    def train_model(self):
        """
        Trains the U-net hybrid loss segmentation model
        :return:
        """
        try:
            data, labels = self.data_loader.load_training_data_clahe()
            inputs, outputs = preprocess_data(data, labels, self.input_shape)

            # idxes = [i for i in range(0, 20)]
            # np.random.shuffle(idxes)
            # train_idx = idxes[:10]
            # val_idx = idxes[-10:]
            #
            # train_inputs = inputs[train_idx]
            # train_outputs = outputs[train_idx]
            # train_inputs, train_outputs = rotate_images(train_inputs, train_outputs)
            # train_rand_idxes = [i for i in range(len(train_inputs))]
            # np.random.shuffle(train_rand_idxes)
            # train_idxes = idxes[:10]
            # train_inputs = inputs[train_idxes]
            # train_outputs = outputs[train_idxes]

            # val_inputs = inputs[val_idx]
            # val_outputs = outputs[val_idx]
            # train_loader = tf.data.Dataset.from_tensor_slices((train_inputs, train_outputs))
            train_loader = tf.data.Dataset.from_tensor_slices((inputs, outputs))
            # validation_loader = tf.data.Dataset.from_tensor_slices((val_inputs, val_outputs))

            logging.info("Preparing batches...")
            batch_size = 1
            train_dataset = (
                train_loader
                    .shuffle(len(inputs))
                    # .shard(num_shards=len(train_inputs) // 10, index=0)
                    .batch(batch_size)
            )

            # validation_dataset = (
            #     validation_loader
            #         .batch(batch_size)
            # )

            logging.info("Loading model...")
            # model = self.get_model()
            # model = self.build_model()
            loss = {'loss_fn': loss_fn, 'dice_coef': dice_coef}
            model = keras.models.load_model(self.model_path + "/" + self.model_name, custom_objects=loss)

            logging.info("Compiling model...")
            model.compile(loss=loss_fn, optimizer='adam', metrics=['accuracy', dice_coef], run_eagerly=True)

            logging.info("Training model...")

            # model.fit(train_dataset, epochs=150)

            scores = model.evaluate(train_dataset, verbose=1)

            print("%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))
            print("%s: %.2f%%" % (model.metrics_names[2], scores[2] * 100))

            # model.save(self.model_path + "/heartsegmodel_lucky.h5")

        except FileNotFoundError as fe:
            logging.error("File not found " + str(fe))
        except PreprocessException as pe:
            # logging.error("Preprocess exception " + str(pe))
            raise pe

    def test_model(self, image):
        """
        Test model on given image
        :param image: image of heart to be segmented
        :return: prediction of the model
        """
        original_size = image.shape
        image = prepare_test_image(image, self.input_shape)

        loss = {'loss_fn': loss_fn, 'dice_coef': dice_coef}
        model = keras.models.load_model(self.model_path + "/" + self.model_name, custom_objects=loss)

        predictions = model.predict(image, batch_size=1, verbose=1)
        labels = tf.argmax(predictions, axis=4).numpy()
        labels = np.reshape(labels, (64, 64, 64))

        rename_map = [0, 205, 420, 500, 550, 600, 820, 850]

        values = []
        for x in range(len(labels)):
            values_x = []
            for y in range(len(labels[x])):
                values_y = []
                for z in range(len(labels[x][y])):
                    values_y.append(rename_map[labels[x][y][z]])
                values_x.append(values_y)
            values.append(values_x)

        values = np.asarray(values)

        prediction = resize(values, original_size, order=0, preserve_range=True, anti_aliasing=False)

        return prediction

