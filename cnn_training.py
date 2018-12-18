"""
使用网络进行训练
"""

import tensorflow as tf
import cnn_inference
from classes.JAFFEDataHelper import *
from classes.CKDataHelper import *

DATASET_TYPE = 'JAFFE'
# 指定训练使用的数据集类型，可为JAFFE或CK+
BATCH_SIZE = 16
# 单轮训练所用数据数量

# 采用衰减学习率
LEARNING_RATE_BASE = 0.01
# 初始学习率
LEARNING_RATE_DECAY = 0.99
# 学习率衰减率
REGULARIZATION_RATE = 0.0003
# 正则化参数
TRAINING_STEPS = 8001
# 训练轮数
MOVING_AVERAGE_DECAY = 0.99
# 滑动平均衰减系数



def JAFFE_train():
    # 在JAFFE数据集上进行训练
    X = np.zeros((BATCH_SIZE, IMAGE_SIZE, IMAGE_SIZE, CHANNEL_NUM), dtype=np.float32)
    Y = np.zeros((BATCH_SIZE, OUTPUT_NUM), dtype=np.float32)
    jaffeDataHelper = JAFFEDataHelper()
    # 获取一个JAFFE帮助类实例
    x = tf.placeholder(tf.float32, [
        BATCH_SIZE,
        IMAGE_SIZE,
        IMAGE_SIZE,
        CHANNEL_NUM], name='x-input')
    y_ = tf.placeholder(tf.float32, [None, OUTPUT_NUM], name='y-input')
    regularizer = tf.contrib.layers.l2_regularizer(REGULARIZATION_RATE)
    # 正则化对象
    y = cnn_inference.inference(x, dropout=True, regularizer=regularizer)
    # 输入神经网络，采用Dropout，且用L2正则化
    global_step = tf.Variable(0, trainable=False)
    variable_averages = tf.train.ExponentialMovingAverage(MOVING_AVERAGE_DECAY, global_step)
    variables_averages_op = variable_averages.apply(tf.trainable_variables())
    # 采用滑动平均
    cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=y, labels=tf.argmax(y_, 1))
    cross_entropy_mean = tf.reduce_mean(cross_entropy)
    # 计算交叉熵
    loss = cross_entropy_mean + tf.add_n(tf.get_collection('losses'))
    # 计算损失函数
    learning_rate = tf.train.exponential_decay(
        LEARNING_RATE_BASE,
        global_step,
        len(jaffeDataHelper._images) / BATCH_SIZE,
        LEARNING_RATE_DECAY,
        staircase=True)
    # 衰减学习率
    train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss, global_step=global_step)
    # 定义优化操作，采用梯度下降优化器
    with tf.control_dependencies([train_step, variables_averages_op]):  # variables_averages_op
        train_op = tf.no_op(name='train')
        # 绑定优化操作与滑动平均操作，统称为train_op
    saver = tf.train.Saver()
    # 模型保存器对象
    with tf.Session() as sess:
        tf.global_variables_initializer().run()
        # 初始化变量
        for i in range(TRAINING_STEPS):
            jaffeDataHelper.get_data(X, Y, BATCH_SIZE)
            # 获取训练数据
            _, loss_value, step = sess.run([train_op, loss, global_step], feed_dict={x: X, y_: Y})
            if i % 100 == 0:
                print("After %d training step(s), loss on training batch is %g." % (step, loss_value))
                saver.save(sess, os.path.join(MODEL_SAVE_PATH, MODEL_NAME), global_step=global_step)
                # 保存模型


def CK_train():
    X = np.zeros((BATCH_SIZE, IMAGE_SIZE, IMAGE_SIZE, CHANNEL_NUM), dtype=np.float32)
    Y = np.zeros((BATCH_SIZE), dtype=np.int64)
    ckDataHelper = CKDataHelper()
    # 获取CK+数据集帮助类对象
    x = tf.placeholder(tf.float32, [
        BATCH_SIZE,
        IMAGE_SIZE,
        IMAGE_SIZE,
        CHANNEL_NUM], name='x-input')
    y_ = tf.placeholder(tf.int64, [BATCH_SIZE], name='y-input')
    regularizer = tf.contrib.layers.l2_regularizer(REGULARIZATION_RATE)
    # 正则化对象
    y = cnn_inference.inference(x, dropout=True, regularizer=regularizer)
    # 输入神经网络，采用Dropout，且用L2正则化
    global_step = tf.Variable(0, trainable=False)
    variable_averages = tf.train.ExponentialMovingAverage(MOVING_AVERAGE_DECAY, global_step)
    variables_averages_op = variable_averages.apply(tf.trainable_variables())
    # 采用滑动平均
    cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=y, labels=y_)
    cross_entropy_mean = tf.reduce_mean(cross_entropy)
    # 计算交叉熵
    loss = cross_entropy_mean + tf.add_n(tf.get_collection('losses'))
    # 计算损失函数
    learning_rate = tf.train.exponential_decay(
        LEARNING_RATE_BASE,
        global_step,
        ckDataHelper._size / BATCH_SIZE,
        LEARNING_RATE_DECAY,
        staircase=True)
    # 采用指数衰减学习率
    train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss, global_step=global_step)
    # 定义优化操作，采用梯度下降优化器
    with tf.control_dependencies([train_step, variables_averages_op]):  # variables_averages_op
        train_op = tf.no_op(name='train')
        # 绑定优化操作与滑动平均操作，统称为train_op

    saver = tf.train.Saver()
    # 模型保存器对象
    with tf.Session() as sess:
        tf.global_variables_initializer().run()
        # 初始化变量
        for i in range(TRAINING_STEPS):
            ckDataHelper.get_data(X, Y, BATCH_SIZE)
            # 获取训练数据
            _, loss_value, step = sess.run([train_op, loss, global_step], feed_dict={x: X, y_: Y})
            if i % 100 == 0:
                print("After %d training step(s), loss on training batch is %g." % (step, loss_value))
                saver.save(sess, os.path.join(MODEL_SAVE_PATH, MODEL_NAME), global_step=global_step)
                # 保存模型


def main(argv=None):
    if DATASET_TYPE == 'JAFFE':
        JAFFE_train()
    elif DATASET_TYPE == 'CK+':
        CK_train()
    else:
        raise Exception('Please set the value of `DATASET_TYPE`')


if __name__ == '__main__':
    tf.app.run()
