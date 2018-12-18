import os
from classes.FaceIdentifier import *
from definitions import *

def CK_catch_faces():
    """
    对本地保存的CK+数据集的所有图片（约10000张）进行截脸操作，并替换原图片
    """
    cnt = 0
    faceIdentifier = FaceIdentifier()
    # 获取人脸识别器实例
    for folder in os.listdir(CK_DIR):
        # 获取数据集文件夹中的所有主体文件夹
        dir2 = os.path.join(CK_DIR, folder)
        for folder2 in os.listdir(dir2):
            # 获取主体文件夹的所有表情序列文件夹
            if not str(folder2)[0] == '.':
                # 用.开头的为无效文件夹
                dir3 = os.path.join(dir2, folder2)
                images = os.listdir(dir3)
                # 获取该表情序列文件夹下的所有图片
                num = len(images)
                # 图片数量
                for i in range(num):
                    image = images[i]
                    if image[0] == '.':
                        # 无效图片
                        i += 1
                        continue
                    cnt += 1
                    print(image, str(cnt / 100) + '%')
                    # 显示当前处理进度百分比，以10000张作为基数
                    cv2.imwrite(os.path.join(dir3, image),
                           faceIdentifier.get_face(cv2.imread(os.path.join(dir3, image))))
                    # 覆盖原图片


if __name__ == '__main__':
    CK_catch_faces()