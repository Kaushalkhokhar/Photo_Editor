import os
import shutil
from PIL import Image
import numpy as np 
import cv2
import matplotlib.pyplot as plt 

APP_ROOT = os.path.dirname(os.path.abspath(__file__)) 
target = os.path.join(APP_ROOT, 'processed_images/') #To store processed image

f = []
for (dirpath, dirnames, filenames) in os.walk(os.path.join(APP_ROOT, 'Images/')):
    f.extend(filenames)

_, file_extension = os.path.splitext(f[0]) #file_extension of uploaded image
image_path = os.path.join(APP_ROOT, 'Images/', f[0]) #path of uploaded image

if os.path.isdir(target):
    shutil.rmtree(target)            
    os.mkdir(target)
else:    
    os.mkdir(target)

def convolution(plotting):     
    img = cv2.imread(image_path)
    kernel = np.ones((5,5),np.float32)/25
    dst = cv2.filter2D(img,-1,kernel)

    filename = convolution.__name__ + file_extension
    destination = "/".join([target, filename])        
    im = Image.fromarray(dst)
    im.save(destination)

    if plotting == True:
        plt.subplot(121),plt.imshow(img),plt.title('Original')
        plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(dst),plt.title('Averaging')
        plt.xticks([]), plt.yticks([])
        plt.show()

    return filename   

def averaging(plotting):   
    img = cv2.imread(image_path)
    blur = cv2.blur(img,(5,5))

    filename = averaging.__name__ + file_extension
    destination = "/".join([target, filename])        
    im = Image.fromarray(blur)
    im.save(destination)

    if plotting == True:
        plt.subplot(121),plt.imshow(img),plt.title('Original')
        plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(blur),plt.title('Averaging')
        plt.xticks([]), plt.yticks([])
        plt.show() 

    return filename    

def gaussian_blur(plotting):    
    img = cv2.imread(image_path)
    blur = cv2.GaussianBlur(img,(5,5),0)

    filename = gaussian_blur.__name__ + file_extension
    destination = "/".join([target, filename])        
    im = Image.fromarray(blur)
    im.save(destination)
    
    if plotting == True:
        plt.subplot(121),plt.imshow(img),plt.title('Original')
        plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(blur),plt.title('Averaging')
        plt.xticks([]), plt.yticks([])
        plt.show()  

    return filename   

def median_blur(plotting):    
    img = cv2.imread(image_path)
    blur = cv2.medianBlur(img,5)

    filename = median_blur.__name__ + file_extension
    destination = "/".join([target, filename])        
    im = Image.fromarray(blur)
    im.save(destination)
    
    if plotting == True:
        plt.subplot(121),plt.imshow(img),plt.title('Original')
        plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(blur),plt.title('Averaging')
        plt.xticks([]), plt.yticks([])
        plt.show()    
    
    return filename 

def bilateral_blur(plotting):   
    img = cv2.imread(image_path)
    blur = cv2.bilateralFilter(img,9,75,75)

    filename = bilateral_blur.__name__ + file_extension
    destination = "/".join([target, filename])        
    im = Image.fromarray(blur)
    im.save(destination)
    
    if plotting == True:
        plt.subplot(121),plt.imshow(img),plt.title('Original')
        plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(blur),plt.title('Averaging')
        plt.xticks([]), plt.yticks([])
        plt.show()    

    return filename 

