import os
from classes.FaceIdentifier import *
from definitions import *
def JAFFE_catch_faces():
    # 对JAFFE所有图片进行截脸并覆盖原图片
    faceIdentifer = FaceIdentifier()
    images = os.listdir(JAFFE_DIR)
    for image in images:
        print(image)
        cv2.imwrite(os.path.join(JAFFE_DIR, image),
                    faceIdentifer.get_face(cv2.imread(os.path.join(JAFFE_DIR, image))))


if __name__ == '__main__':
    JAFFE_catch_faces()