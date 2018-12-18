# 宏定义文件

IMAGE_SIZE = 32
# 输入神经网络的图片大小
CHANNEL_NUM = 1
# 图片频道数
OUTPUT_NUM = 6
# 输出结点数

# EXPRESSIONS = ['Anger', 'Contempt', 'Disgust', 'Fear', 'Happy', 'Sadness', 'Surprise']
EXPRESSIONS = ['Anger', 'Disgust', 'Fear', 'Happy', 'Sadness', 'Surprise']
# 表情和序号的对应关系


JAFFE_DIR = r'C:\Users\HP\PycharmProjects\FacialExpressionIdentifier\datasets\JAFFE'
# JAFFE数据集目录
JAFFE_LABEL_DIR = r'C:\Users\HP\PycharmProjects\FacialExpressionIdentifier\datasets\JAFFE_labels.txt'
# JAFFE数据集的Label文件目录


CK_DIR = 'H:\CK\cohn-kanade-images'
# CK+数据集目录
CK_LABEL_DIR = 'H:\CK\Emotion'
# CK+数据集的Label目录
CK_SAMPLE_MAX_NUM = 10708
# CK+数据集图片总数量


FACE_CLASSIFIER_DIR = r"C:\Users\HP\PycharmProjects\FacialExpressionIdentifier\haarcascade_frontalface_alt2.xml"
# 脸部识别器目录
VALIDATE_DIR = 'C:/Users/HP/PycharmProjects/FacialExpressionIdentifier/validate'
# 验证数据目录

MODEL_SAVE_PATH = "C:/Users/HP/PycharmProjects/FacialExpressionIdentifier/models"
# 模型保存目录
MODEL_NAME = "model"
# 模型名

INTERVAL = 0.2
# 从视频中获取帧的间隔大小（单位：秒）