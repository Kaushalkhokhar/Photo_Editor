import os, shutil, cv2
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

class image_operations():
    def __init__(self):        
        self.APP_ROOT = os.path.dirname(os.path.abspath(__file__)) 
        self.processed_image = os.path.join(self.APP_ROOT, 'processed_images/') #To store processed image

        self.file_original = []
        for (dirpath, dirnames, filenames) in os.walk(os.path.join(self.APP_ROOT, 'Original/')):
            self.file_original.extend(filenames)

        #self.file_original = os.listdir(os.path.join(self.APP_ROOT, 'Images/'))

        self.file_id, self.file_extension = os.path.splitext(self.file_original[0]) #self.file_extension of uploaded image
        self.image_path = os.path.join(self.APP_ROOT, 'Original/', self.file_original[0]) #path of uploaded image        

    def convolution(self, plotting):           
        img = cv2.imread(self.image_path)
        '''if len(img.shape) == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)''' #To convert color iamge to gray scale 
        
        kernel = np.ones((5,5),np.float32)/25
        dst = cv2.filter2D(img,-1,kernel)

        filename = image_operations.convolution.__name__ + self.file_id + self.file_extension
        destination = "/".join([self.processed_image, filename])        
        im = Image.fromarray(dst)
        im.save(destination)        

        if plotting == True:
            plt.subplot(121),plt.imshow(img),plt.title('Original')
            plt.xticks([]), plt.yticks([])
            plt.subplot(122),plt.imshow(dst),plt.title('Averaging')
            plt.xticks([]), plt.yticks([])
            plt.show()        

        return filename   

    def averaging(self, plotting):   
        img = cv2.imread(self.image_path)
        '''if len(img.shape) == 3:  
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)'''
        blur = cv2.blur(img,(5,5))

        filename = image_operations.averaging.__name__ + self.file_id + self.file_extension
        destination = "/".join([self.processed_image, filename])        
        im = Image.fromarray(blur)
        im.save(destination)

        if plotting == True:
            plt.subplot(121),plt.imshow(img),plt.title('Original')
            plt.xticks([]), plt.yticks([])
            plt.subplot(122),plt.imshow(blur),plt.title('Averaging')
            plt.xticks([]), plt.yticks([])
            plt.show() 

        return filename    

    def gaussian_blur(self, plotting):    
        img = cv2.imread(self.image_path)
        '''if len(img.shape) == 3: 
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)'''
        blur = cv2.GaussianBlur(img,(5,5),0)

        filename = image_operations.gaussian_blur.__name__ + self.file_id + self.file_extension
        destination = "/".join([self.processed_image, filename])        
        im = Image.fromarray(blur)
        im.save(destination)
        
        if plotting == True:
            plt.subplot(121),plt.imshow(img),plt.title('Original')
            plt.xticks([]), plt.yticks([])
            plt.subplot(122),plt.imshow(blur),plt.title('Averaging')
            plt.xticks([]), plt.yticks([])
            plt.show()  

        return filename   

    def median_blur(self, plotting):    
        img = cv2.imread(self.image_path)
        '''if len(img.shape) == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)'''
        blur = cv2.medianBlur(img,5)

        filename = image_operations.median_blur.__name__ + self.file_id + self.file_extension
        destination = "/".join([self.processed_image, filename])        
        im = Image.fromarray(blur)
        im.save(destination)
        
        if plotting == True:
            plt.subplot(121),plt.imshow(img),plt.title('Original')
            plt.xticks([]), plt.yticks([])
            plt.subplot(122),plt.imshow(blur),plt.title('Averaging')
            plt.xticks([]), plt.yticks([])
            plt.show()    
        
        return filename 

    def bilateral_blur(self, plotting):   
        img = cv2.imread(self.image_path)
        '''if len(img.shape) == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)'''
        blur = cv2.bilateralFilter(img,9,75,75)

        filename = image_operations.bilateral_blur.__name__ + self.file_id + self.file_extension
        destination = "/".join([self.processed_image, filename])        
        im = Image.fromarray(blur)
        im.save(destination)
        
        if plotting == True:
            plt.subplot(121),plt.imshow(img),plt.title('Original')
            plt.xticks([]), plt.yticks([])
            plt.subplot(122),plt.imshow(blur),plt.title('Averaging')
            plt.xticks([]), plt.yticks([])
            plt.show()    

        return filename