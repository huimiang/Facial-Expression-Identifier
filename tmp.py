# 用来随便测试代码的临时文件

import cv2
import numpy as np
a = np.zeros((1, 624, 650, 1), dtype=np.uint8)
a[0] = np.reshape(cv2.cvtColor(cv2.imread('./dog.png'), cv2.COLOR_BGR2GRAY), (624, 650, 1))
print(np.shape(a[0]))
cv2.imshow('asd', a[0])
cv2.waitKey(0)
