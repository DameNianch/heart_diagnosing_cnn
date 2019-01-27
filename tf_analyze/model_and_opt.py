import tensorflow as tf
import numpy as np

def initilizer(var_shape, var_type):
    if var_type == "conv":
        using_initilizer = tf.contrib.layers.xavier_initializer_conv2d()
    elif var_type == "bias":
        using_initilizer = tf.contrib.layers.xavier_initializer()
    return using_initilizer(var_shape)

def conv_variables_maker(conv_shape, filter_name):
    conv_var = tf.Variable(initilizer(conv_shape, "conv"), name=filter_name)
    return conv_var

def bias_variables_maker():
    return 0


def graph_tf(input_place, drop_rate_place, NUM_CLASS):

    with tf.name_scope('adjust-data-layer'):
        x_0 = tf.reshape(input_place, [1, 1, 270, 1])

    with tf.name_scope('1st-layer'):
        x = x_0
        y = tf.nn.conv2d(x, filter=conv_variables_maker([1, 31, 1, NUM_CLASS], "1st-conv"), strides=[1, 1, 30, 1], dilations=[1, 1, 1, 1], padding="VALID")
        z = tf.nn.relu(y)
        z = tf.nn.avg_pool(z, ksize=[1, 1, 8, 1], strides=[1, 1, 1, 1], padding="VALID")
        z = tf.reshape(z, [1, NUM_CLASS])
        z = tf.nn.softmax(z)

    z_out = z

    return z_out


def loss_calc(labels, logits):
    cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels=labels, logits=logits.op.outputs[0]))
    return cross_entropy

def train_opt(loss_calc, learning_rate):
    training_steps = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss_calc)
    return training_steps

def valid_acc_calc(labels, logits, NUM_CLASS):
    acc = tf.metrics.mean_per_class_accuracy(labels=labels, predictions=logits, num_classes=NUM_CLASS)
    return acc

