import cv2
import numpy as np

#load images
im_1 =cv2.resize(cv2.imread('test1.jpg', 0), (320,320))
im_2 =cv2.resize(cv2.imread('test2.jpg', 0), (320,320))
im_3 =cv2.resize(cv2.imread('test3.jpg', 0), (320,320))


diff = cv2.subtract(im_3,im_1)
diff = np.mean(diff)/255
print('Error Between img 3 and 1')
print(diff)

diff = cv2.subtract(im_3,im_2)
diff = np.mean(diff)/255
print('Error Between img 3 and 2')
print(diff)