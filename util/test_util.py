import cv2
from definitions import *
# 两个测试工具函数
# 用以测试指定的矩阵是否正确存储了图像与Label

def CK_test(X, Y):
    for i in range(len(X)):
        image = X[i]
        label = Y[i]
        cv2.imshow('Test Show', image)
        print(EXPRESSIONS[label])
        cv2.waitKey(0)

def JAFFE_test(X, Y):
    for i in range(len(X)):
        image = X[i]
        label = Y[i]
        cv2.imshow('Test Show', image)
        for j in range(len(label)):
            print(EXPRESSIONS[j], label[j], sep=': ', end=' ')
        print()
        cv2.waitKey(0)