import cv2
from definitions import *
class VideoHelper:
    # 处理视频的帮助类
    def __init__(self):
        pass

    def get_images(self, video_dir):
        images = []
        frame_count = 0
        # 计数器
        capture = cv2.VideoCapture(video_dir)
        fps = capture.get(cv2.CAP_PROP_FPS)
        # 得到视频的FPS
        success, frame = capture.read()
        # success表示读取是否成功，frame表示读取的帧
        cnt = 0
        while (success):
            frame_count += 1
            if frame is not None and frame_count > fps * INTERVAL:
                # 每INTERVAL秒保存一个帧
                cnt += 1
                print('frame' + str(cnt) + ' loaded')
                frame_count -= fps * INTERVAL
                images.append(frame)
            success, frame = capture.read()
        capture.release()
        return images


if __name__ == '__main__':
    # 测试该类的正确性
    videoHelper = VideoHelper()
    image = videoHelper.get_images('H:/123.mp4')

