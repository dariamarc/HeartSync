import keras.models
import numpy as np
import tensorflow as tf
import tensorflow_cloud as tfc
from src.data.load_data import load_training_data_ct, load_data
from src.data.transform_data import preprocess_data
from src.model.losses import loss_fn
from src.utils.ops import read_transfer_weights

def conv3D(input, output, kernel_size, strides):

    return tf.keras.layers.Conv3D(filters=output, kernel_size=kernel_size, strides=strides, padding="same",
                                  data_format="channels_last",
                                  kernel_initializer=tf.keras.initializers.TruncatedNormal(mean=0.0, stddev=0.01),
                                  kernel_regularizer=tf.keras.regularizers.l2(0.0005),
                                  use_bias=False)(input)


def deconv3D(input, output):
    return tf.keras.layers.Conv3DTranspose(filters=output, kernel_size=4, padding="same", strides=[2, 2, 2],
                                           kernel_regularizer=tf.keras.regularizers.l2(0.0005))(input)


def build_model():
    '''
    Modelul U-net cu loss hibrid
    :return:
    '''
    k = tf.keras

    input = k.layers.Input(shape=(64, 64, 64, 1))

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

    concat1 = k.layers.concatenate([deconv1_relu, conv4_2])
    deconv1_2 = conv3D(input=concat1, output=256, kernel_size=3, strides=1)
    deconv1_bn_2 = k.layers.BatchNormalization(epsilon=1e-5, scale=True, momentum=0.9)(deconv1_2)
    deconv1_relu_2 = k.layers.ReLU()(deconv1_bn_2)

    deconv2 = deconv3D(input=deconv1_relu_2, output=256)
    deconv2_bn = k.layers.BatchNormalization(epsilon=1e-5, scale=True, momentum=0.9)(deconv2)
    deconv2_relu = k.layers.ReLU()(deconv2_bn)

    concat2 = k.layers.concatenate([deconv2_relu, conv3])
    deconv2_2 = conv3D(input=concat2, output=128, kernel_size=3, strides=1)
    deconv2_bn_2 = k.layers.BatchNormalization(epsilon=1e-5, scale=True, momentum=0.9)(deconv2_2)
    deconv2_relu_2 = k.layers.ReLU()(deconv2_bn_2)

    deconv3 = deconv3D(input=deconv2_relu_2, output=128)
    deconv3_bn = k.layers.BatchNormalization(epsilon=1e-5, scale=True, momentum=0.9)(deconv3)
    deconv3_relu = k.layers.ReLU()(deconv3_bn)

    concat3 = k.layers.concatenate([deconv3_relu, conv2])
    deconv3_2 = conv3D(input=concat3, output=64, kernel_size=3, strides=1)
    deconv3_bn_2 = k.layers.BatchNormalization(epsilon=1e-5, scale=True, momentum=0.9)(deconv3_2)
    deconv3_relu_2 = k.layers.ReLU()(deconv3_bn_2)

    deconv4 = deconv3D(input=deconv3_relu_2, output=64)
    deconv4_bn = k.layers.BatchNormalization(epsilon=1e-5, scale=True, momentum=0.9)(deconv4)
    deconv4_relu = k.layers.ReLU()(deconv4_bn)

    concat4 = k.layers.concatenate([deconv4_relu, conv1])
    deconv4_2 = conv3D(input=concat4, output=32, kernel_size=3, strides=1)
    deconv4_bn_2 = k.layers.BatchNormalization(epsilon=1e-5, scale=True, momentum=0.9)(deconv4_2)
    deconv4_relu_2 = k.layers.ReLU()(deconv4_bn_2)

    output = k.layers.Conv3D(8, kernel_size=1, strides=1)(deconv4_relu_2)
    prob = k.layers.Softmax()(output)

    model = k.models.Model(inputs=input, outputs=prob)

    print(model.summary())

    return model


def get_model():
    '''
    Model pentru antrenarea pe laptopul meu local (mult mai putine layere)
    :return:
    '''
    k = tf.keras

    input_layer = k.Input(shape=(64, 64, 64, 1))

    conv1 = conv3D(input=input_layer, output=64, kernel_size=3, strides=1)
    conv1_bn = k.layers.BatchNormalization(epsilon=1e-5, scale=True, momentum=0.9)(conv1)
    conv1_relu = k.layers.ReLU()(conv1_bn)
    pool1 = k.layers.MaxPool3D(pool_size=2, strides=2)(conv1_relu)

    # conv5 = conv3D(input=pool1, output=128, kernel_size=3, strides=1)
    # conv5_bn = k.layers.BatchNormalization(epsilon=1e-5, scale=True, momentum=0.9)(conv5)
    # conv5_relu = k.layers.ReLU()(conv5_bn)
    # conv5_2 = conv3D(input=conv5_relu, output=128, kernel_size=3, strides=1)
    # conv5_bn_2 = k.layers.BatchNormalization(epsilon=1e-5, scale=True, momentum=0.9)(conv5_2)
    # conv5_relu_2 = k.layers.ReLU()(conv5_bn_2)
    #
    deconv1 = deconv3D(input=pool1, output=64)
    deconv1_bn = k.layers.BatchNormalization(epsilon=1e-5, scale=True, momentum=0.9)(deconv1)
    deconv1_relu = k.layers.ReLU()(deconv1_bn)

    concat1 = k.layers.concatenate([deconv1_relu, conv1])
    deconv1_2 = conv3D(input=concat1, output=32, kernel_size=3, strides=1)
    deconv1_bn_2 = k.layers.BatchNormalization(epsilon=1e-5, scale=True, momentum=0.9)(deconv1_2)
    deconv1_relu_2 = k.layers.ReLU()(deconv1_bn_2)

    output = k.layers.Conv3D(8, kernel_size=1, strides=1)(deconv1_relu_2)
    prob = k.layers.Softmax()(output)
    # pred_labels = tf.argmax(prob, axis=4)

    model = k.models.Model(inputs=input_layer, outputs=prob)

    print(model.summary())

    return model



def train_model():
    data, labels = load_data()
    inputs, outputs = preprocess_data(data, labels)

    inputs = np.reshape(inputs, (20, 64, 64, 64, 1))
    outputs = np.reshape(outputs, (20, 64, 64, 64, 1))
    train_loader = tf.data.Dataset.from_tensor_slices((inputs, outputs))

    print("Preparing batches...")
    batch_size = 1
    # Augment on the fly during training.
    train_dataset = (
        train_loader.shuffle(len(inputs))
            # .map(train_preprocessing)
            .batch(batch_size)
            # .prefetch(2)
    )

    print("Loading model...")
    model = get_model()

    print("Compiling model...")
    model.compile(loss=loss_fn, optimizer='adam', metrics=['accuracy'], run_eagerly=True)

    print("Training model...")
    model.fit(train_dataset, epochs=30, verbose=2)

    # outputs = [layer.output for layer in model.layers]

    # scores = model.evaluate(inputs, outputs, verbose=0)
    # print("%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))

    model.save('heartseg_model.h5')


def test_model(image):

    model = keras.models.load_model('heartseg_model.h5')

    prediction = model.predict(image)

    return prediction
