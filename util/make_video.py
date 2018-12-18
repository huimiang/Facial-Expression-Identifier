import os
import cv2
import time


# 该函数用以通过一连串图片序列来合成视频，以满足该系统的测试需要
def make_video():
    path = r'H:\CK\cohn-kanade-images2\S501\004'
    # 图片序列的路径
    size = (720, 480)
    # 指定图片的分辨率
    file_list = os.listdir(path)
    # 获取该目录下的所有文件名
    fps = 30
    # 设定目标视频的FPS
    file_path = r"C:/Users/hp/Desktop/" + str(int(time.time())) + ".avi"
    # 设定视频的导出路径
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    videoWriter = cv2.VideoWriter(file_path, fourcc, fps, size)
    # 获取一个VideoWriter实例
    for item in file_list:
        if item.endswith('.png'):
            # 判断图片后缀是否是.png
            item = path + '/' + item
            image = cv2.imread(item)
            # 读取图片
            videoWriter.write(image)
            # 把图片写进视频

    videoWriter.release()
    # 释放对象

if __name__ == '__main__':
    make_video()
