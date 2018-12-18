import tensorflow as tf
import cnn_inference
import cnn_training
from classes.JAFFEDataHelper import *
from classes.CKDataHelper import *
from classes.FaceIdentifier import *
from classes.VideoHelper import *
import time

EVALUATION_BATCH_SIZE = 5
# 单次测试所用数据数量
EVALUATION_TURNS = 10
# 测试轮数

class Evaluator:
    # 对神经网络的评估器
    def __init__(self):
        self._faceIdentifier = FaceIdentifier()
        self._videoHelper = VideoHelper()

    def evaluate_video(self, video_dir):
        """
        对给定视频进行测试
        :param video_dir: 视频路径
        :return: 神经网络的输出结果，以及对哪些帧是正常的哪些帧是异常进行记录的flags列表
        """
        images = self._videoHelper.get_images(video_dir)
        print('IMAGES GOT')
        length = len(images)
        X = np.zeros((length, IMAGE_SIZE, IMAGE_SIZE, CHANNEL_NUM), dtype=np.float32)
        # 初始化一个矩阵
        flags = [True] * length
        for i in range(length):
            if len(np.shape(images[i])) != 2:
                # 若是三通道彩色图，转为单通道黑白图
                image = cv2.cvtColor(images[i], cv2.COLOR_BGR2GRAY)
            else:
                image = images[i]
            try:
                # 尝试获取人脸
                image = self._faceIdentifier.get_face(image)
            except:
                # 捕捉到异常，说明要么获取了多个人脸，要么找不到人脸
                # 在这里不终止程序，而是用一个flags列表记录哪些帧是捕捉到异常了的
                flags[i] = False
            image = cv2.resize(image, (IMAGE_SIZE, IMAGE_SIZE))
            # 调整图片大小
            tmp = np.reshape(image, (IMAGE_SIZE, IMAGE_SIZE, CHANNEL_NUM))
            # 调整矩阵维度，如32, 32转为32, 32, 1以满足神经网络输入需要
            # 以下代码用来测试截取结果
            # cv2.imshow('test', tmp)
            # cv2.waitKey(0)
            cv2.normalize(tmp, X[i], alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
            # 归一化操作
        print('DATUM GOT')
        x = tf.placeholder(tf.float32, [
            length,
            IMAGE_SIZE,
            IMAGE_SIZE,
            CHANNEL_NUM], name='x-input')
        # 定义占位符
        y = tf.nn.softmax(cnn_inference.inference(x, dropout=False, regularizer=None))
        # 神经网络推断，因为不是测试过程，所以不需要dropout与regularizer
        variable_averages = tf.train.ExponentialMovingAverage(cnn_training.MOVING_AVERAGE_DECAY)
        variables_to_restore = variable_averages.variables_to_restore()
        saver = tf.train.Saver(variables_to_restore)
        # 准备读取模型，这里事先读取好之前的滑动平均模型
        with tf.Session() as sess:
            # 开启会话
            ckpt = tf.train.get_checkpoint_state(MODEL_SAVE_PATH)
            if ckpt and ckpt.model_checkpoint_path:
                # 若找到模型cheakpoint
                saver.restore(sess, ckpt.model_checkpoint_path)
                # 读取模型
                res = sess.run(y, feed_dict={x: X})
                # 启动网络
                print('Output Result of CNN:', res)
                return res, flags
                # 返回结果以及标记列表
            else:
                raise Exception('No checkpoint file found')
                # 找不到存档，抛出异常

    def evaluate_one(self, image_dir):
        """
        对给定图片进行测试
        :param image_dir: 图片路径
        :return: 返回一个字符串和一个列表。
        字符串为将给定图片进行预处理后的结果保存的路径地址（若出现异常则为异常信息）
        列表为神经网络的输出结果
        """
        source_image = cv2.imdecode(np.fromfile(image_dir, dtype=np.uint8), -1)
        # imread不支持中文路径，需要通过numpy中转
        if len(np.shape(source_image)) != 2:
            # 若是三通道彩色图，转为单通道黑白图
            image = cv2.cvtColor(source_image, cv2.COLOR_BGR2GRAY)
        else:
            image = source_image
        try:
            image = self._faceIdentifier.get_face(image)
            # 尝试获取脸部
        except Exception as e:
            # 获取失败，直接返回错误信息，函数结束
            return str(e), None
        image = cv2.resize(image, (IMAGE_SIZE, IMAGE_SIZE))
        # 调整图像大小
        X = np.zeros((1, IMAGE_SIZE, IMAGE_SIZE, CHANNEL_NUM), dtype=np.float32)
        # 初始化一个矩阵
        tmp = np.reshape(image, (IMAGE_SIZE, IMAGE_SIZE, CHANNEL_NUM))
        # 调整矩阵维度
        cv2.normalize(tmp, X[0], alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
        # 归一化
        x = tf.placeholder(tf.float32, [
            1,
            IMAGE_SIZE,
            IMAGE_SIZE,
            CHANNEL_NUM], name='x-input')
        # 声明占位符
        y = tf.nn.softmax(cnn_inference.inference(x, False, None))
        # 神经网络推断
        variable_averages = tf.train.ExponentialMovingAverage(cnn_training.MOVING_AVERAGE_DECAY)
        variables_to_restore = variable_averages.variables_to_restore()
        saver = tf.train.Saver(variables_to_restore)
        # 准备读取模型
        with tf.Session() as sess:
            # 开启会话
            ckpt = tf.train.get_checkpoint_state(MODEL_SAVE_PATH)
            if ckpt and ckpt.model_checkpoint_path:
                # 找到模型checkpoint
                saver.restore(sess, ckpt.model_checkpoint_path)
                res = sess.run(y, feed_dict={x: X})[0]
                # 返回值y是一个二维矩阵，所以要加[0]获取里面内层的数据
                print('Output Result of CNN:', res)
                name = time.asctime(time.localtime(time.time())).replace(' ', '_').replace(':', '_')
                name = 'cache/' + name + '.jpg'
                # 生一个文件名，文件名与当前系统时间有关，文件目录为根目录下的cache文件夹
                cv2.imwrite(name, tmp)
                # 写文件
                print('Imaged saved with directory:', name)
                return name, res
            else:
                raise Exception('No checkpoint file found')

    def evaluate_on_JAFFE(self):
        # 在JAFFE数据集的测试集上进行测试，这里的测试集是没有作为神经网络的训练集的
        # 因此可以准确评估网络性能
        X = np.zeros((EVALUATION_BATCH_SIZE, IMAGE_SIZE, IMAGE_SIZE, CHANNEL_NUM), dtype=np.float32)
        Y = np.zeros((EVALUATION_BATCH_SIZE, OUTPUT_NUM), dtype=np.float32)
        x = tf.placeholder(tf.float32, [
            EVALUATION_BATCH_SIZE,
            IMAGE_SIZE,
            IMAGE_SIZE,
            CHANNEL_NUM], name='x-input')
        y_ = tf.placeholder(tf.int64, [EVALUATION_BATCH_SIZE, OUTPUT_NUM], name='y-input')
        y = cnn_inference.inference(x, False, None)
        correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        # 得到正确率
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
                # 实例化一个JAFFE数据集帮助对象
                print('EVALUATION BATCH SIZE:', EVALUATION_BATCH_SIZE)
                for i in range(EVALUATION_TURNS):
                    jaffeDataHelper.get_test_data(X, Y, EVALUATION_BATCH_SIZE)
                    accuracy_score = sess.run(accuracy, feed_dict={x: X, y_: Y})
                    print("BATCH " + str(i + 1) + " Validation accuracy = %g" % (accuracy_score))
            else:
                raise Exception('No checkpoint file found')

    # def validate_on_CK(self):
    #     # with tf.Graph().as_default() as g:
    #     X = np.zeros((EVALUATION_BATCH_SIZE, IMAGE_SIZE, IMAGE_SIZE, CHANNEL_NUM), dtype=np.uint8)
    #     Y = np.zeros((EVALUATION_BATCH_SIZE), dtype=np.float32)
    #     x = tf.placeholder(tf.float32, [
    #         EVALUATION_BATCH_SIZE,
    #         IMAGE_SIZE,
    #         IMAGE_SIZE,
    #         CHANNEL_NUM], name='x-input')
    #     y_ = tf.placeholder(tf.int64, [EVALUATION_BATCH_SIZE], name='y-input')
    #     y = LeNet5Inference.inference(x, False, None)
    #     correct_prediction = tf.equal(tf.argmax(y, 1), y_)
    #     accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    #     # variable_averages = tf.train.ExponentialMovingAverage(LeNet5_training.MOVING_AVERAGE_DECAY)
    #     # variables_to_restore = variable_averages.variables_to_restore()
    #     # saver = tf.train.Saver(variables_to_restore)
    #     saver = tf.train.Saver()
    #     with tf.Session() as sess:
    #         ckpt = tf.train.get_checkpoint_state(MODEL_SAVE_PATH)
    #         if ckpt and ckpt.model_checkpoint_path:
    #             saver.restore(sess, ckpt.model_checkpoint_path)
    #             # global_step = ckpt.model_checkpoint_path.split('/')[-1].split('-')[-1]
    #             ckDataHelper = CKDataHelper()
    #             print('EVALUATION BATCH SIZE:', EVALUATION_BATCH_SIZE)
    #             for i in range(EVALUATION_TURNS):
    #                 ckDataHelper.get_test_data(X, Y, EVALUATION_BATCH_SIZE)
    #                 accuracy_score = sess.run(accuracy, feed_dict={x: X, y_: Y})
    #                 print("BATCH " + str(i + 1) + " Validation accuracy = %g" % (accuracy_score))
    #         else:
    #             raise Exception('No checkpoint file found')


if __name__ == '__main__':
    evaluator = Evaluator()
    # evaluator.evaluate_video('H://234.mp4')
    evaluator.evaluate_on_JAFFE()
