import os
import numpy as np 
import cv2
import matplotlib.pyplot as plt 

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

def convolution(filename, plotting):    
    image_path = os.path.join(APP_ROOT, 'Images/', filename)
    img = cv2.imread(image_path)

    kernel = np.ones((5,5),np.float32)/25
    dst = cv2.filter2D(img,-1,kernel)

    if plotting == True:
        plt.subplot(121),plt.imshow(img),plt.title('Original')
        plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(dst),plt.title('Averaging')
        plt.xticks([]), plt.yticks([])
        plt.show()

    return dst



