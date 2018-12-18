import tensorflow as tf
from definitions import *

CONV1_FILTER_SIZE = 5
# 第一个卷积层的过滤器宽度
CONV1_DEEP = 6
# 第一个卷积层的深度

CONV2_FILTER_SIZE = 5
# 第二个卷积层的过滤器宽度
CONV2_DEEP = 16
# 第二个卷积层的深度

CONV3_FILTER_SIZE = 5
# 第三个卷积层的过滤器宽度
CONV3_DEEP = 120
# 第三个卷积层的深度

FC1_OUTPUT_NUM = 84
# 第一个全连接层的输出结点数量

FC2_INPUT_NUM = 1660
# FC2_INPUT_NUM = 8188
# 第二个全连接层的输入结点数量


def inference(input_tensor, dropout, regularizer):
    # 神经网络推断
    with tf.variable_scope('layer1-conv1', reuse=tf.AUTO_REUSE):
        """
        第一层，卷积层1
        输入矩阵维度为(BATCH_SIZE, 32, 32, 1)
        输出矩阵维度为(BATCH_SIZE, 28，28, 6)
        """
        conv1_weights = tf.get_variable(
            "weight", [CONV1_FILTER_SIZE, CONV1_FILTER_SIZE, CHANNEL_NUM, CONV1_DEEP],
            initializer=tf.truncated_normal_initializer(stddev=0.1))
        conv1_biases = tf.get_variable("bias", [CONV1_DEEP], initializer=tf.constant_initializer(0.0))
        conv1 = tf.nn.conv2d(input_tensor, conv1_weights, strides=[1, 1, 1, 1], padding='VALID')
        conv1_res = tf.nn.bias_add(conv1, conv1_biases)
        relu1 = tf.nn.relu(conv1_res)

    with tf.name_scope("layer2-pool1"):
        """
        第二层，池化层1
        输入矩阵维度为(BATCH_SIZE, 28, 28, 6)
        输出矩阵维度为(BATCH_SIZE, 14, 14, 6)
        """
        pool1 = tf.nn.max_pool(relu1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding="VALID")

    with tf.variable_scope("layer3-conv2", reuse=tf.AUTO_REUSE):
        """
        第三层，卷积层2
        输入矩阵维度为(BATCH_SIZE, 14, 14, 6)
        输出矩阵维度为(BATCH_SIZE, 10, 10, 16)
        """
        conv2_weights = tf.get_variable(
            "weight", [CONV2_FILTER_SIZE, CONV2_FILTER_SIZE, CONV1_DEEP, CONV2_DEEP],
            initializer=tf.truncated_normal_initializer(stddev=0.1))
        conv2_biases = tf.get_variable("bias", [CONV2_DEEP], initializer=tf.constant_initializer(0.0))
        conv2 = tf.nn.conv2d(pool1, conv2_weights, strides=[1, 1, 1, 1], padding='VALID')
        conv2_res = tf.nn.bias_add(conv2, conv2_biases)
        relu2 = tf.nn.relu(conv2_res)

    with tf.name_scope("layer4-pool2"):
        """
        第四层，池化层2
        输入矩阵维度为(BATCH_SIZE, 10, 10, 16)
        输出矩阵维度为(BATCH_SIZE, 5, 5, 16)
        """
        pool2 = tf.nn.max_pool(relu2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='VALID')

    with tf.variable_scope("layer5-conv3", reuse=tf.AUTO_REUSE):
        """
        第五层，卷积层3
        输入矩阵维度为(BATCH_SIZE, 5, 5, 16)
        输出矩阵维度为(BATCH_SIZE, 1, 1, 120)
        """
        conv3_weights = tf.get_variable(
            "weight", [CONV3_FILTER_SIZE, CONV3_FILTER_SIZE, CONV2_DEEP, CONV3_DEEP],
            initializer=tf.truncated_normal_initializer(stddev=0.1))
        conv3_biases = tf.get_variable("bias", [CONV3_DEEP], initializer=tf.constant_initializer(0.0))
        conv3 = tf.nn.conv2d(pool2, conv3_weights, strides=[1, 1, 1, 1], padding='VALID')
        conv3_res = tf.nn.bias_add(conv3, conv3_biases)
        relu3 = tf.nn.relu(conv3_res)

    with tf.variable_scope('layer6-fc1', reuse=tf.AUTO_REUSE):
        """
        第六层，全连接层1
        输入矩阵维度为(BATCH_SIZE, 120)
        输出矩阵维度为(BATCH_SIZE, 84)
        """
        conv3_shape = conv3.get_shape().as_list()
        conv3_nodes = conv3_shape[1] * conv3_shape[2] * conv3_shape[3]
        conv3_reshaped = tf.reshape(relu3, [conv3_shape[0], conv3_nodes])

        fc1_weights = tf.get_variable("weight", [conv3_nodes, FC1_OUTPUT_NUM],
                                      initializer=tf.truncated_normal_initializer(stddev=0.1))
        if regularizer != None:
            tf.add_to_collection('losses', regularizer(fc1_weights))
        fc1_biases = tf.get_variable("bias", [FC1_OUTPUT_NUM], initializer=tf.constant_initializer(0.1))
        fc1 = tf.nn.relu(tf.matmul(conv3_reshaped, fc1_weights) + fc1_biases)
        if dropout:
            fc1 = tf.nn.dropout(fc1, 0.5)

    with tf.variable_scope('layer7-fc2', reuse=tf.AUTO_REUSE):
        """
        第七层，全连接层2，采用跨连接
        输入矩阵维度为(BATCH_SIZE, 1660)
        输出矩阵维度为(BATCH_SIZE, 6)
        """
        pool1_shape = pool1.get_shape().as_list()
        pool1_nodes = pool1_shape[1] * pool1_shape[2] * pool1_shape[3]
        pool1_reshaped = tf.reshape(pool1, [pool1_shape[0], pool1_nodes])

        pool2_shape = pool2.get_shape().as_list()
        pool2_nodes = pool2_shape[1] * pool2_shape[2] * pool2_shape[3]
        pool2_reshaped = tf.reshape(pool2, [pool2_shape[0], pool2_nodes])

        fc2_input = tf.concat([fc1, pool1_reshaped, pool2_reshaped], 1)
        fc2_weights = tf.get_variable("weight", [FC2_INPUT_NUM, OUTPUT_NUM],
                                      initializer=tf.truncated_normal_initializer(stddev=0.1))
        if regularizer != None:
            tf.add_to_collection('losses', regularizer(fc2_weights))
        fc2_biases = tf.get_variable("bias", [OUTPUT_NUM], initializer=tf.constant_initializer(0.1))
        logit = tf.matmul(fc2_input, fc2_weights) + fc2_biases
    return logit
