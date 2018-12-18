import cv2
from definitions import *
class FaceIdentifier:
    # 人脸识别器
    def __init__(self):
        self._classifier = cv2.CascadeClassifier(FACE_CLASSIFIER_DIR)
        # 初始化一个分类器实例

    def get_face(self, image):
        """
        :param image: 需要截取人脸的矩阵
        :return: 截取结果
        """
        faces = self._classifier.detectMultiScale(image)
        if len(faces) == 0:
            # 找不到人脸
            # cv2.imshow('show', image)
            # # 窗口显示找不到人脸的图片
            # cv2.waitKey(0)
            print('-----ERROR: No Face Found-----')
            raise Exception('No Face Found')
            # 抛出异常
        elif len(faces) > 1:
            # 找到多个人脸
            print('-----ERROR: Multiple Faces Found-----')
            raise Exception('Multiple Faces Found')
            # 抛出异常
        return image[faces[0][1]:faces[0][1] + faces[0][3], faces[0][0]:faces[0][0] + faces[0][2]]

if __name__ == '__main__':
    image = cv2.imread(r'C:\Users\HP\PycharmProjects\FacialExpressionIdentifier\datasets\JAFFE_bakcup\KA.FE4.48.tiff')
    faceIdentifier = FaceIdentifier()
    cv2.imshow('Test', faceIdentifier.get_face(image))
    cv2.waitKey(0)


