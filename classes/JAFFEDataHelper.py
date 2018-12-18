import os
import cv2
import numpy as np
import random
from definitions import *


class JAFFEDataHelper:
    # JAFFE数据集帮助类
    def __init__(self):
        self._images = os.listdir(JAFFE_DIR)
        # JAFFE图片列表
        self._test_images = os.listdir(VALIDATE_DIR)
        # JAFFE测试图片列表
        self._dic = {}
        # 记录图片与Label关系的字典
        self.load_data()
        # 从Label文件中读取上述字典

    def load_data(self):
        # 从Label文件中读取上述字典
        with open(JAFFE_LABEL_DIR, 'r+') as f:
            line = f.readline()
            while line:
                name = line.split()[-1]
                name = name.replace('-', '')
                labels = [(i) for i in line.split()[1: -1]]
                self._dic[name] = self.order_labels(labels)
                # 因为CK+数据集与JAFFE数据集的Label顺序（即各情绪的序号）不同，在此进行修正
                line = f.readline()

    @staticmethod
    def order_labels(labels):
        # 修正Label编号
        order = [3, 4, 5, 0, 1, 2]
        # 两数据集的Label编号对应关系
        ordered_labels = [0] * OUTPUT_NUM
        for i in range(len(labels)):
            ordered_labels[order[i]] = labels[i]
        return ordered_labels

    @staticmethod
    def handle_data():
        # 对JAFFE所有图片进行截脸并覆盖原图片
        from util import jaffe_data_handle
        jaffe_data_handle.JAFFE_catch_faces()

    def get_data(self, X, Y, n):
        """
        从JAFFE数据集获取数据存到给定矩阵中
        :param X: numpy(n, IMAGE_SIZE, IMAGE_SIZE, CHANNEL_NUM), 输入矩阵
        :param Y: numpy(n), 结果矩阵
        :param n: int, 需要获取的数据数量
        :return:
        """
        if len(X) != n or len(Y) != n:
            # 输入矩阵的维度不符合规范
            raise Exception('Illegal Length of Lists')
        if n > len(self._images):
            # 要求的数据多于数据集总数据
            raise Exception('JAFFE Samples Out of Range')
        random_order = random.sample(range(0, len(self._images)), n)
        # 获取随机采样序列
        for i in range(n):
            image = self._images[random_order[i]]
            name = str(image).replace('.', '')[: 5]
            if not self._dic.__contains__(name):
                # 找不到Label，抛出异常
                print('Label Not Found of File:', name)
                raise Exception('No Label Found')
            Y[i] = self._dic[name]
            tmp = cv2.resize(cv2.imread(os.path.join(JAFFE_DIR, image)), (IMAGE_SIZE, IMAGE_SIZE))
            # 缩放
            tmp2 = np.reshape(cv2.cvtColor(tmp, cv2.COLOR_BGR2GRAY), (IMAGE_SIZE, IMAGE_SIZE, CHANNEL_NUM))
            # 变更频道数同时更改维度
            cv2.normalize(tmp2, X[i], alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
            # 归一化

    def get_test_data(self, X, Y, n):
        """
        从JAFFE测试数据集中获取测试数据存到给定矩阵中
        :param X: numpy(n, IMAGE_SIZE, IMAGE_SIZE, CHANNEL_NUM), 输入矩阵
        :param Y: numpy(n), 结果矩阵
        :param n: int, 需要获取的测试数据数量
        :return:
        """
        if len(X) != n or len(Y) != n:
            # 输入矩阵的维度不符合规范
            raise Exception('Illegal Length of Lists')
        if n > len(self._test_images):
            # 要求的数据多于数据集总数据
            raise Exception('Test Samples Out of Range')
        random_order = random.sample(range(0, len(self._test_images)), n)
        # 获取随机采样序列
        for i in range(n):
            image = self._test_images[random_order[i]]
            name = str(image).replace('.', '')[: 5]
            if not self._dic.__contains__(name):
                # 找不到Label，抛出异常
                print('Label Not Found of File:', name)
                raise Exception('No Label Found')
            Y[i] = self._dic[name]
            tmp = cv2.resize(cv2.imread(os.path.join(VALIDATE_DIR, image)), (IMAGE_SIZE, IMAGE_SIZE))
            # 缩放
            tmp2 = np.reshape(cv2.cvtColor(tmp, cv2.COLOR_BGR2GRAY), (IMAGE_SIZE, IMAGE_SIZE, CHANNEL_NUM))
            # 频道数变为1且更改维度
            cv2.normalize(tmp2, X[i], alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
            # 归一化


if __name__ == '__main__':
    # 测试此类的正确性
    from util import test_util
    jaffeDataHelper = JAFFEDataHelper()
    test_num = 100
    X = np.zeros((test_num, IMAGE_SIZE, IMAGE_SIZE, CHANNEL_NUM), dtype=np.float32)
    Y = np.zeros((test_num, OUTPUT_NUM), dtype=np.float32)
    jaffeDataHelper.get_data(X, Y, test_num)
    test_util.JAFFE_test(X, Y)
