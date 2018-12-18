import pymysql
import cv2
import numpy as np
from definitions import *
import random


class CKDataHelper:
    # 获取CK+训练数据集的帮助类
    def __init__(self):
        db = pymysql.connect('localhost', 'root', '123456', 'train')
        # 连接数据库
        self._cursor = db.cursor()
        self._sql = """select i.addr, g.emotion 
            from imgs i, `groups` g 
            where i.subject = g.subject and i.group = g.group and g.emotion <> 0 
                and g.num - i.no <= 3 and g.emotion <> 2;"""
        # 多表连接，SELECT图片路径以及表情编号，获取每一表情序列的倒数三张图片
        self._cursor.execute(self._sql)
        self._size = len(self._cursor.fetchall())
        # 查询结果的条数
        self.random_move()
        # 随机游标的初始位置

    @staticmethod
    def load_data():
        # 将CK+数据库信息导入数据库
        from util import database_load
        database_load.load_data()

    @staticmethod
    def handle_data():
        # 将CK+数据库的所有图片截取脸部后替换原图片
        from util import ck_data_handle
        ck_data_handle.CK_catch_faces()


    def random_move(self):
        # 随机将游标移动若干个位置(10-30)
        move_steps = random.randint(10, 30)
        for _ in range(move_steps):
            row = self._cursor.fetchone()
            if not row:
                # 已经移动到末尾，重置游标
                self._cursor.scroll(0, mode='absolute')

    def get_data(self, X, Y, n):
        """
        从CK+数据集获取数据存到给定矩阵中
        :param X: numpy(n, IMAGE_SIZE, IMAGE_SIZE, CHANNEL_NUM), 输入矩阵
        :param Y: numpy(n), 结果矩阵
        :param n: int, 需要获取的数据数量
        :return:
        """
        if len(X) != n or len(Y) != n:
            # 输入矩阵或输出矩阵的维度不符合要求
            raise Exception('Illegal Length of Lists')
        if n > self._size:
            # 试图获取的数据数量超出SQL查询结果
            raise Exception('CK+ Samples Out of Range')
        for i in range(n):
            self.random_move()
            # 随机游标位置
            row = self._cursor.fetchone()
            # 获取一条查询结果
            while not row:
                # 若查询结果为空，继续随机直到不为空
                self.random_move()
                row = self._cursor.fetchone()
            tmp = cv2.resize(cv2.imread(row[0]), (IMAGE_SIZE, IMAGE_SIZE))
            # 缩放图片
            tmp2 = np.reshape(cv2.cvtColor(tmp, cv2.COLOR_BGR2GRAY), (IMAGE_SIZE, IMAGE_SIZE, CHANNEL_NUM))
            # 变更频道数同时调整维度
            cv2.normalize(tmp2, X[i], alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
            # 矩阵归一化
            Y[i] = row[1] - 1
            # 获取情绪编号，因为不考虑中立情绪0，所有后面的情绪编号依次往前移一位
            if Y[i] != 0:
                # 因为不考虑Contempt这一在CK+与JAFFE并不都有的情绪，而Contempt编号本来为2，所以后面的还要再前移
                Y[i] -= 1


if __name__ == '__main__':
    # 测试该类的正确性
    ckDataHelper = CKDataHelper()
    test_steps = 1000
    test_batch_size = 100
    X = np.zeros((test_batch_size, IMAGE_SIZE, IMAGE_SIZE, CHANNEL_NUM), dtype=np.float32)
    Y = np.zeros((test_batch_size), dtype=np.uint8)
    from util import test_util
    for i in range(test_steps):
        ckDataHelper.get_data(X, Y, test_batch_size)
        test_util.CK_test(X, Y)
