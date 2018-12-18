import tensorflow as tf

import cnn_inference
import cnn_training
from classes.CKDataHelper import *
from classes.JAFFEDataHelper import *

TEST_BATCH_SIZE = 100
TEST_TURNS = 10



def validate_on_CK():
    # 在CK+的所有数据集上随机进行验证
    X = np.zeros((TEST_BATCH_SIZE, IMAGE_SIZE, IMAGE_SIZE, CHANNEL_NUM), dtype=np.float32)
    Y = np.zeros((TEST_BATCH_SIZE), dtype=np.float32)
    # 两个输入矩阵
    x = tf.placeholder(tf.float32, [
        TEST_BATCH_SIZE,
        IMAGE_SIZE,
        IMAGE_SIZE,
        CHANNEL_NUM], name='x-input')
    y_ = tf.placeholder(tf.int64, [TEST_BATCH_SIZE], name='y-input')
    # 定义占位符
    y = cnn_inference.inference(x, False, None)
    # 神经网络推断
    correct_prediction = tf.equal(tf.argmax(y, 1), y_)
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    # 正确率
    variable_averages = tf.train.ExponentialMovingAverage(cnn_training.MOVING_AVERAGE_DECAY)
    variables_to_restore = variable_averages.variables_to_restore()
    saver = tf.train.Saver(variables_to_restore)
    # saver = tf.train.Saver()
    with tf.Session() as sess:
        ckpt = tf.train.get_checkpoint_state(MODEL_SAVE_PATH)
        if ckpt and ckpt.model_checkpoint_path:
            saver.restore(sess, ckpt.model_checkpoint_path)
            # global_step = ckpt.model_checkpoint_path.split('/')[-1].split('-')[-1]
            ckDataHelper = CKDataHelper()
            print('TEST BATCH SIZE:', TEST_BATCH_SIZE)
            for i in range(TEST_TURNS):
                ckDataHelper.get_data(X, Y, TEST_BATCH_SIZE)
                # 获取数据
                accuracy_score = sess.run(accuracy, feed_dict={x : X, y_: Y})
                print("BATCH " + str(i + 1) + " Validation accuracy = %g" % (accuracy_score))
        else:
            raise Exception('No checkpoint file found')


def validate_on_JAFFE():
    # 在JAFFE数据集上进行随机验证
    X = np.zeros((TEST_BATCH_SIZE, IMAGE_SIZE, IMAGE_SIZE, CHANNEL_NUM), dtype=np.float32)
    Y = np.zeros((TEST_BATCH_SIZE, OUTPUT_NUM), dtype=np.float32)
    # 输入矩阵
    x = tf.placeholder(tf.float32, [
        TEST_BATCH_SIZE,
        IMAGE_SIZE,
        IMAGE_SIZE,
        CHANNEL_NUM], name='x-input')
    y_ = tf.placeholder(tf.int64, [TEST_BATCH_SIZE, OUTPUT_NUM], name='y-input')
    # 定义占位符
    y = cnn_inference.inference(x, False, None)
    correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    # 正确率
    variable_averages = tf.train.ExponentialMovingAverage(cnn_training.MOVING_AVERAGE_DECAY)
    variables_to_restore = variable_averages.variables_to_restore()
    saver = tf.train.Saver(variables_to_restore)
    # saver = tf.train.Saver()
    with tf.Session() as sess:
        ckpt = tf.train.get_checkpoint_state(MODEL_SAVE_PATH)
        if ckpt and ckpt.model_checkpoint_path:
            saver.restore(sess, ckpt.model_checkpoint_path)
            # global_step = ckpt.model_checkpoint_path.split('/')[-1].split('-')[-1]
            jaffeDataHelper = JAFFEDataHelper()
            print('TEST BATCH SIZE:', TEST_BATCH_SIZE)
            for i in range(TEST_TURNS):
                jaffeDataHelper.get_data(X, Y, TEST_BATCH_SIZE)
                # 获取数据
                accuracy_score = sess.run(accuracy, feed_dict={x : X, y_: Y})
                print("BATCH " + str(i + 1) + " Validation accuracy = %g" % (accuracy_score))
        else:
            raise Exception('No checkpoint file found')


def main(argv=None):
    print('ON CK:')
    validate_on_CK()
    print('---------------')
    print('ON JAFFE')
    validate_on_JAFFE()


if __name__ == '__main__':
    main()