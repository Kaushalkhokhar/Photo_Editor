import os, shutil, cv2, random
from PIL import Image
import numpy as np
from web_app import APP_ROOT, admin_user
from web_app.model import Methods

class Image_processing():
    def __init__(self):
        pass        
        '''APP_ROOT = os.path.dirname(os.path.abspath(__file__)) 
        processed_image = os.path.join(APP_ROOT, 'processed_images/') #To store processed image        

        file_original = os.listdir(os.path.join(APP_ROOT, 'Original/'))
        file_second = os.listdir(os.path.join(APP_ROOT, 'Second/'))

        file_id, file_extension = os.path.splitext(file_original[0]) #file_extension of uploaded image
        image_path = os.path.join(APP_ROOT, 'Original/', file_original[0]) #path of uploaded image  
        image_path_2 = os.path.join(APP_ROOT, 'Second/', file_second[0])'''      
        
        '''file_original = os.listdir(original)        
        file_id, file_extension = os.path.splitext(file_original[0]) #file_extension of uploaded image
        image_path = os.path.join(original, file_original[0]) #path of uploaded image ''' 
            

    def convolution(self):           
        img = cv2.imread(image_path)
        '''if len(img.shape) == 2:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)''' #To convert color iamge to gray scale 
        
        kernel = np.ones((5,5),np.float32)/25
        dst = cv2.filter2D(img,-1,kernel)

        filename = image_operations.convolution.__name__ + file_id + file_extension
        destination = "/".join([result, filename])        
        im = Image.fromarray(dst)
        im.save(destination)

        return filename   

    def averaging(self):   
        img = cv2.imread(image_path)
        '''if len(img.shape) == 3:  
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)'''
        blur = cv2.blur(img,(5,5))

        filename = image_operations.averaging.__name__ + file_id + file_extension
        destination = "/".join([result, filename])        
        im = Image.fromarray(blur)
        im.save(destination)        

        return filename    

    def gaussian_blur(self):    
        img = cv2.imread(image_path)
        '''if len(img.shape) == 3: 
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)'''
        blur = cv2.GaussianBlur(img,(5,5),0)

        filename = image_operations.gaussian_blur.__name__ + file_id + file_extension
        destination = "/".join([result, filename])        
        im = Image.fromarray(blur)
        im.save(destination)

        return filename   

    def median_blur(self):    
        img = cv2.imread(image_path)
        '''if len(img.shape) == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)'''
        blur = cv2.medianBlur(img,5)

        filename = image_operations.median_blur.__name__ + file_id + file_extension
        destination = "/".join([result, filename])        
        im = Image.fromarray(blur)
        im.save(destination)

        return filename 

    def bilateral_blur(self):   
        img = cv2.imread(image_path)
        '''if len(img.shape) == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)'''
        blur = cv2.bilateralFilter(img,9,75,75)

        filename = image_operations.bilateral_blur.__name__ + file_id + file_extension
        destination = "/".join([result, filename])        
        im = Image.fromarray(blur)
        im.save(destination)

        return filename
    
    @staticmethod
    def filter(img, filter_type, kernal):
        if filter_type == "Averaging":
            if kernal == "5*5_First" or kernal == "5*5_Second":
                output = cv2.blur(img,(5,5))
            elif kernal == "7*7_First" or kernal == "7*7_Second":
                output = cv2.blur(img,(7,7))
            elif kernal == "9*9_First" or kernal == "9*9_Second":
                output = cv2.blur(img,(9,9))
            else:
                output = cv2.blur(img,(3,3))

            
        elif filter_type == "Gaussian_Blur":
            if kernal == "5*5_First":
                output = cv2.GaussianBlur(img,(5,5),0)
            elif kernal == "5*5_Second":
                output = cv2.GaussianBlur(img,(5,5),0.5)
            elif kernal == "7*7_First":
                output = cv2.GaussianBlur(img,(7,7),0)
            elif kernal == "7*7_Second":
                output = cv2.GaussianBlur(img,(7,7),0.5)
            elif kernal == "9*9_First":
                output = cv2.GaussianBlur(img,(9,9),0)
            elif kernal == "9*9_Second":
                output = cv2.GaussianBlur(img,(9,9),0.5)
            elif kernal == "3*3_First":
                output = cv2.GaussianBlur(img,(3,3),0)
            else:
                output = cv2.GaussianBlur(img,(3,3),0.5)

        elif filter_type == "Median_Blur":
            if kernal == "5*5_First" or kernal == "5*5_Second":
                output = cv2.medianBlur(img,5)
            elif kernal == "7*7_First" or kernal == "7*7_Second":
                output = cv2.medianBlur(img,7)
            elif kernal == "9*9_First" or kernal == "9*9_Second":
                output = cv2.medianBlur(img,9)             
            else:
                output = cv2.medianBlur(img,3)

        elif filter_type == "Bilateral_Blur":
            if kernal == "5*5_First":
                output = cv2.bilateralFilter(img,5,60,60)
            elif kernal == "5*5_Second":
                output = cv2.bilateralFilter(img,5,110,110)
            elif kernal == "7*7_First":
                output = cv2.bilateralFilter(img,7,60,60)
            elif kernal == "7*7_Second":
                output = cv2.bilateralFilter(img,7,110,110)
            elif kernal == "9*9_First":
                output = cv2.bilateralFilter(img,9,60,60)
            elif kernal == "9*9_Second":
                output = cv2.bilateralFilter(img,9,110,110)
            elif kernal == "3*3_First":
                output = cv2.bilateralFilter(img,3,60,60)
            else:
                output = cv2.bilateralFilter(img,3,110,110)

        elif filter_type == "HPF":
            if kernal == "3*3_First":
                kernal = 0 - (np.ones((3,3), np.float32))
                kernal[1,1] = 8
                kernal = kernal
                output = cv2.filter2D(img, -1, kernal)
            elif kernal == "3*3_Second":
                kernal = 0 - (np.ones((3,3), np.float32))
                kernal[1,1] = 12
                kernal[1,0], kernal[1,2], kernal[0,1], kernal[2,1] = [-2,-2,-2,-2]
                kernal = kernal
                output = cv2.filter2D(img, -1, kernal)
            elif kernal == "5*5_First":
                kernal = 0 - ((np.ones((5,5), np.float32)))
                kernal[2,2] = 24
                kernal[1,2], kernal[3,2], kernal[2,1], kernal[2,3] = [-1,-1,-1,-1]
                kernal[1,1], kernal[1,3], kernal[3,1], kernal[3,3] = [-1,-1,-1,-1]
                kernal = kernal
                output = cv2.filter2D(img, -1, kernal)
            elif kernal == "5*5_Second":
                kernal = 0 - (np.ones((5,5), np.float32))
                kernal[2,2] = 26
                kernal[1,2], kernal[3,2], kernal[2,1], kernal[2,3] = [-2,-2,-2,-2]
                kernal[1,1], kernal[1,3], kernal[3,1], kernal[3,3] = [-1,-1,-1,-1]
                kernal = kernal
                output = cv2.filter2D(img, -1, kernal)
            elif kernal == "7*7_First":
                kernal = 0 - ((np.ones((7,7), np.float32)))
                kernal[3,3] = 98
                kernal[3,2], kernal[3,4], kernal[2,3], kernal[4,3] = [-8,-8,-8,-8]
                kernal[2,2], kernal[2,4], kernal[4,2], kernal[4,4] = [-4,-4,-4,-4]
                kernal[1,1], kernal[1,2], kernal[1,3], kernal[1,4], kernal[1,5] = [-2,-2,-2,-2,-2]
                kernal[5,1], kernal[5,2], kernal[5,3], kernal[5,4], kernal[5,5] = [-2,-2,-2,-2,-2]
                kernal[2,1], kernal[3,1], kernal[4,1] = [-2,-2,-2]
                kernal[2,5], kernal[3,5], kernal[4,5] = [-2,-2,-2]
                kernal = kernal
                output = cv2.filter2D(img, -1, kernal)
            elif kernal == "7*7_Second":
                kernal = 0 - (np.ones((7,7), np.float32))
                kernal[3,3] = 64
                kernal[3,2], kernal[3,4], kernal[2,3], kernal[4,3] = [-4,-4,-4,-4]
                kernal[2,2], kernal[2,4], kernal[4,2], kernal[4,4] = [-2,-2,-2,-2]
                kernal[1,1], kernal[1,2], kernal[1,3], kernal[1,4], kernal[1,5] = [-1,-1,-1,-1,-1]
                kernal[5,1], kernal[5,2], kernal[5,3], kernal[5,4], kernal[5,5] = [-1,-1,-1,-1,-1]
                kernal[2,1], kernal[3,1], kernal[4,1] = [-1,-1,-1]
                kernal[2,5], kernal[3,5], kernal[4,5] = [-1,-1,-1]
                kernal = kernal
                output = cv2.filter2D(img, -1, kernal)
            elif kernal == "9*9_First":
                kernal = 0 - ((np.ones((9,9), np.float32)))
                kernal[4,4] = 218
                kernal[4,3], kernal[4,5], kernal[3,4], kernal[5,4] = [-16,-16,-16,-16]
                kernal[3,3], kernal[3,5], kernal[5,3], kernal[5,5] = [-8,-8,-8,-8]
                kernal[2,2], kernal[2,3], kernal[2,4], kernal[2,5], kernal[2,6] = [-4,-4,-4,-4,-4]
                kernal[6,2], kernal[6,3], kernal[6,4], kernal[6,5], kernal[6,6] = [-4,-4,-4,-4,-4]
                kernal[3,2], kernal[4,2], kernal[5,2] = [-4,-4,-4]
                kernal[3,6], kernal[4,6], kernal[5,6] = [-4,-4,-4]
                kernal[1,1], kernal[1,2], kernal[1,3], kernal[1,4], kernal[1,5], kernal[1,6], kernal[1,7] = [-2,-2,-2,-2,-2,-2,-2]
                kernal[7,1], kernal[7,7], kernal[7,3], kernal[7,4], kernal[7,5], kernal[7,6], kernal[7,7] = [-2,-2,-2,-2,-2,-2,-2]
                kernal[2,1], kernal[3,1], kernal[4,1], kernal[5,1], kernal[6,1] = [-2,-2,-2,-2,-2]
                kernal[2,7], kernal[3,7], kernal[4,7], kernal[5,7], kernal[6,7] = [-2,-2,-2,-2,-2]                
                output = cv2.filter2D(img, -1, kernal)
            elif kernal == "9*9_Second":
                kernal = 0 - (np.ones((9,9), np.float32))
                kernal[4,4] = 124
                kernal[4,3], kernal[4,5], kernal[3,4], kernal[5,4] = [-8,-8,-8,-8]
                kernal[3,3], kernal[3,5], kernal[5,3], kernal[5,5] = [-4,-4,-4,-4]
                kernal[2,2], kernal[2,3], kernal[2,4], kernal[2,5], kernal[2,6] = [-2,-2,-2,-2,-2]
                kernal[6,2], kernal[6,3], kernal[6,4], kernal[6,5], kernal[6,6] = [-2,-2,-2,-2,-2]
                kernal[3,2], kernal[4,2], kernal[5,2] = [-2,-2,-2]
                kernal[3,6], kernal[4,6], kernal[5,6] = [-2,-2,-2]
                kernal[1,1], kernal[1,2], kernal[1,3], kernal[1,4], kernal[1,5], kernal[1,6], kernal[1,7] = [-1,-1,-1,-1,-1,-1,-1]
                kernal[7,1], kernal[7,7], kernal[7,3], kernal[7,4], kernal[7,5], kernal[7,6], kernal[2,7] = [-1,-1,-1,-1,-1,-1,-1]
                kernal[2,1], kernal[3,1], kernal[4,1], kernal[5,1], kernal[6,1] = [-1,-1,-1,-1,-1]
                kernal[2,7], kernal[3,7], kernal[4,7], kernal[5,7], kernal[6,7] = [-1,-1,-1,-1,-1]
                kernal = kernal         
                output = cv2.filter2D(img, -1, kernal)
            elif kernal == "11*11_First":
                kernal = 0 - ((np.ones((11,11), np.float32)))
                kernal[5,5] = 400
                kernal[5,4], kernal[5,6], kernal[4,5], kernal[6,5] = [-32,-32,-32,-32]
                kernal[4,4], kernal[4,6], kernal[6,4], kernal[6,6] = [-16,-16,-16,-16]
                kernal[3,3], kernal[3,4], kernal[3,5], kernal[3,6], kernal[3,7] = [-8,-8,-8,-8,-8]
                kernal[7,3], kernal[7,4], kernal[7,5], kernal[7,6], kernal[7,7] = [-8,-8,-8,-8,-8]
                kernal[6,3], kernal[4,3], kernal[5,3] = [-8,-8,-8]
                kernal[6,7], kernal[4,7], kernal[5,7] = [-8,-8,-8]
                kernal[2,2], kernal[2,3], kernal[2,4], kernal[2,5], kernal[2,6], kernal[2,7], kernal[2,8] = [-4,-4,-4,-4,-4,-4,-4]
                kernal[8,2], kernal[8,3], kernal[8,4], kernal[8,5], kernal[8,6], kernal[8,7], kernal[8,8] = [-4,-4,-4,-4,-4,-4,-4]
                kernal[3,2], kernal[4,2], kernal[5,2], kernal[6,2], kernal[7,2] = [-4,-4,-4,-4,-4]
                kernal[2,8], kernal[3,8], kernal[4,8], kernal[5,8], kernal[6,8] = [-4,-4,-4,-4,-4]
                kernal[1,1], kernal[1,2], kernal[1,3], kernal[1,4], kernal[1,5], kernal[1,6], kernal[1,7], kernal[1,8], kernal[1,9] = [-2,-2,-2,-2,-2,-2,-2,-2,-2]
                kernal[9,1], kernal[9,2], kernal[9,3], kernal[9,4], kernal[9,5], kernal[9,6], kernal[9,7], kernal[9,8], kernal[9,9] = [-2,-2,-2,-2,-2,-2,-2,-2,-2]
                kernal[2,1], kernal[3,1], kernal[4,1], kernal[5,1], kernal[6,1], kernal[7,1], kernal[8,1] = [-2,-2,-2,-2,-2,-2,-2]
                kernal[2,9], kernal[3,9], kernal[4,9], kernal[5,9], kernal[6,9], kernal[7,9], kernal[8,9] = [-2,-2,-2,-2,-2,-2,-2]                
                output = cv2.filter2D(img, -1, kernal)
            else:
                kernal = 0 - (np.ones((11,11), np.float32))
                kernal[5,5] = 200
                kernal[5,4], kernal[5,6], kernal[4,5], kernal[6,5] = [-16,-16,-16,-16]
                kernal[4,4], kernal[4,6], kernal[6,4], kernal[6,6] = [-8,-8,-8,-8]
                kernal[3,3], kernal[3,4], kernal[3,5], kernal[3,6], kernal[3,7] = [-4,-4,-4,-4,-4]
                kernal[7,3], kernal[7,4], kernal[7,5], kernal[7,6], kernal[7,7] = [-4,-4,-4,-4,-4]
                kernal[6,3], kernal[4,3], kernal[5,3] = [-4,-4,-4]
                kernal[6,7], kernal[4,7], kernal[5,7] = [-4,-4,-4]
                kernal[2,2], kernal[2,3], kernal[2,4], kernal[2,5], kernal[2,6], kernal[2,7], kernal[2,8] = [-2,-2,-2,-2,-2,-2,-2]
                kernal[8,2], kernal[8,3], kernal[8,4], kernal[8,5], kernal[8,6], kernal[8,7], kernal[8,8] = [-2,-2,-2,-2,-2,-2,-2]
                kernal[3,2], kernal[4,2], kernal[5,2], kernal[6,2], kernal[7,2] = [-2,-2,-2,-2,-2]
                kernal[2,8], kernal[3,8], kernal[4,8], kernal[5,8], kernal[6,8] = [-2,-2,-2,-2,-2]
                kernal[1,1], kernal[1,2], kernal[1,3], kernal[1,4], kernal[1,5], kernal[1,6], kernal[1,7], kernal[1,8], kernal[1,9] = [-1,-1,-1,-1,-1,-1,-1,-1,-1]
                kernal[9,1], kernal[9,2], kernal[9,3], kernal[9,4], kernal[9,5], kernal[9,6], kernal[9,7], kernal[9,8], kernal[9,9] = [-1,-1,-1,-1,-1,-1,-1,-1,-1]
                kernal[2,1], kernal[3,1], kernal[4,1], kernal[5,1], kernal[6,1], kernal[7,1], kernal[8,1] = [-1,-1,-1,-1,-1,-1,-1]
                kernal[2,9], kernal[3,9], kernal[4,9], kernal[5,9], kernal[6,9], kernal[7,9], kernal[8,9] = [-1,-1,-1,-1,-1,-1,-1]                
                output = cv2.filter2D(img, -1, kernal)
            
        elif filter_type == 'LPF':
            if kernal == "3*3_First":
                kernal = (np.ones((3,3), np.float32))
                kernal[1,1] = 8
                kernal = kernal/9
                output = cv2.filter2D(img, -1, kernal)
            elif kernal == "3*3_Second":
                kernal = (np.ones((3,3), np.float32))
                kernal[1,1] = 12
                kernal[1,0], kernal[1,2], kernal[0,1], kernal[2,1] = [2,2,2,2]
                kernal = kernal/32
                output = cv2.filter2D(img, -1, kernal)
            elif kernal == "5*5_First":
                kernal = (np.ones((5,5), np.float32))
                kernal[2,2] = 8
                kernal = kernal/22
                output = cv2.filter2D(img, -1, kernal)
            elif kernal == "5*5_Second":
                kernal = (np.ones((5,5), np.float32))
                kernal[2,2] = 12
                kernal[1,2], kernal[3,2], kernal[2,1], kernal[2,3] = [2,2,2,2]
                kernal[1,1], kernal[1,3], kernal[3,1], kernal[3,3] = [1,1,1,1]
                kernal = kernal/32
                output = cv2.filter2D(img, -1, kernal)
            elif kernal == "7*7_First":
                kernal = (np.ones((7,7), np.float32))
                kernal[3,3] = 8
                kernal = kernal/36
                output = cv2.filter2D(img, -1, kernal)
            elif kernal == "7*7_Second":
                kernal = (np.ones((7,7), np.float32))
                kernal[3,3] = 24
                kernal[3,2], kernal[3,4], kernal[2,3], kernal[4,3] = [4,4,4,4]
                kernal[2,2], kernal[2,4], kernal[4,2], kernal[4,4] = [2,2,2,2]
                kernal[1,1], kernal[1,2], kernal[1,3], kernal[1,4], kernal[1,5] = [1,1,1,1,1]
                kernal[5,1], kernal[5,2], kernal[5,3], kernal[5,4], kernal[5,5] = [1,1,1,1,1]
                kernal[2,1], kernal[3,1], kernal[4,1] = [1,1,1]
                kernal[2,5], kernal[3,5], kernal[4,5] = [1,1,1]
                kernal = kernal/64
                output = cv2.filter2D(img, -1, kernal)
            elif kernal == "9*9_First":
                kernal = (np.ones((9,9), np.float32))
                kernal[4,4] = 8
                kernal = kernal/52
                output = cv2.filter2D(img, -1, kernal)
            elif kernal == "9*9_Second":
                kernal = (np.ones((9,9), np.float32))
                kernal[4,4] = 48
                kernal[4,3], kernal[4,5], kernal[3,4], kernal[5,4] = [8,8,8,8]
                kernal[3,3], kernal[3,5], kernal[5,3], kernal[5,5] = [4,4,4,4]
                kernal[2,2], kernal[2,3], kernal[2,4], kernal[2,5], kernal[2,6] = [2,2,2,2,2]
                kernal[6,2], kernal[6,3], kernal[6,4], kernal[6,5], kernal[6,6] = [2,2,2,2,2]
                kernal[3,2], kernal[4,2], kernal[5,2] = [2,2,2]
                kernal[3,6], kernal[4,6], kernal[5,6] = [2,2,2]
                kernal[1,1], kernal[1,2], kernal[1,3], kernal[1,4], kernal[1,5], kernal[1,6], kernal[1,7] = [1,1,1,1,1,1,1]
                kernal[7,1], kernal[7,7], kernal[7,3], kernal[7,4], kernal[7,5], kernal[7,6], kernal[2,7] = [1,1,1,1,1,1,1]
                kernal[2,1], kernal[3,1], kernal[4,1], kernal[5,1], kernal[6,1] = [1,1,1,1,1]
                kernal[2,7], kernal[3,7], kernal[4,7], kernal[5,7], kernal[6,7] = [1,1,1,1,1]
                kernal=kernal/128               
                output = cv2.filter2D(img, -1, kernal)
            elif kernal == "11*11_First":
                kernal = (np.ones((11,11), np.float32))
                kernal[5,5] = 8
                kernal = kernal/96  
                output = cv2.filter2D(img, -1, kernal)
            else:
                kernal = (np.ones((11,11), np.float32))
                kernal[5,5] = 64
                kernal[5,4], kernal[5,6], kernal[4,5], kernal[6,5] = [16,16,16,16]
                kernal[4,4], kernal[4,6], kernal[6,4], kernal[6,6] = [8,8,8,8]
                kernal[3,3], kernal[3,4], kernal[3,5], kernal[3,6], kernal[3,7] = [4,4,4,4,4]
                kernal[7,3], kernal[7,4], kernal[7,5], kernal[7,6], kernal[7,7] = [4,4,4,4,4]
                kernal[6,3], kernal[4,3], kernal[5,3] = [4,4,4]
                kernal[6,7], kernal[4,7], kernal[5,7] = [4,4,4]
                kernal[2,2], kernal[2,3], kernal[2,4], kernal[2,5], kernal[2,6], kernal[2,7], kernal[2,8] = [2,2,2,2,2,2,2]
                kernal[8,2], kernal[8,3], kernal[8,4], kernal[8,5], kernal[8,6], kernal[8,7], kernal[8,8] = [2,2,2,2,2,2,2]
                kernal[3,2], kernal[4,2], kernal[5,2], kernal[6,2], kernal[7,2] = [2,2,2,2,2]
                kernal[2,8], kernal[3,8], kernal[4,8], kernal[5,8], kernal[6,8] = [2,2,2,2,2]
                kernal[1,1], kernal[1,2], kernal[1,3], kernal[1,4], kernal[1,5], kernal[1,6], kernal[1,7], kernal[1,8], kernal[1,9] = [1,1,1,1,1,1,1,1,1]
                kernal[9,1], kernal[9,2], kernal[9,3], kernal[9,4], kernal[9,5], kernal[9,6], kernal[9,7], kernal[9,8], kernal[9,9] = [1,1,1,1,1,1,1,1,1]
                kernal[2,1], kernal[3,1], kernal[4,1], kernal[5,1], kernal[6,1], kernal[7,1], kernal[8,1] = [1,1,1,1,1,1,1]
                kernal[2,9], kernal[3,9], kernal[4,9], kernal[5,9], kernal[6,9], kernal[7,9], kernal[8,9] = [1,1,1,1,1,1,1]                
                kernal=kernal/256
                output = cv2.filter2D(img, -1, kernal)

        elif filter_type == 'BPF':
            if kernal == "3*3_First":
                kernal = (np.ones((3,3), np.float32))
                kernal[1,1] = 8
                kernal1 = kernal/9

                kernal = (np.ones((3,3), np.float32))
                kernal[1,1] = 4
                kernal[1,0], kernal[1,2], kernal[0,1], kernal[2,1] = [2,2,2,2]
                kernal2 = kernal/16

                output = cv2.filter2D(img, -1, kernal1-kernal2)
            elif kernal == "3*3_Second":
                kernal = (np.ones((3,3), np.float32))
                kernal[1,1] = 8
                kernal1 = kernal/9

                kernal = (np.ones((3,3), np.float32))
                kernal[1,1] = 4
                kernal[1,0], kernal[1,2], kernal[0,1], kernal[2,1] = [2,2,2,2]
                kernal2 = kernal/3

                output = cv2.filter2D(img, -1, kernal2-kernal1)
            elif kernal == "5*5_First":
                kernal = (np.ones((5,5), np.float32))
                kernal[2,2] = 8
                kernal1 = kernal/9

                kernal = (np.ones((5,5), np.float32))
                kernal[2,2] = 4
                kernal[1,2], kernal[3,2], kernal[2,1], kernal[2,3] = [2,2,2,2]
                kernal[1,1], kernal[1,3], kernal[3,1], kernal[3,3] = [1,1,1,1]
                kernal2 = kernal/16

                output = cv2.filter2D(img, -1, kernal1-kernal2)
            elif kernal == "5*5_Second":
                kernal = (np.ones((5,5), np.float32))
                kernal[2,2] = 8
                kernal1 = kernal/9

                kernal = (np.ones((5,5), np.float32))
                kernal[2,2] = 4
                kernal[1,2], kernal[3,2], kernal[2,1], kernal[2,3] = [2,2,2,2]
                kernal[1,1], kernal[1,3], kernal[3,1], kernal[3,3] = [1,1,1,1]
                kernal2 = kernal/3
                output = cv2.filter2D(img, -1, kernal2-kernal1)
            elif kernal == "7*7_First":
                kernal = (np.ones((7,7), np.float32))
                kernal[3,3] = 8
                kernal1 = kernal/9

                kernal = (np.ones((7,7), np.float32))
                kernal[3,3] = 8
                kernal[3,2], kernal[3,4], kernal[2,3], kernal[4,3] = [4,4,4,4]
                kernal[2,2], kernal[2,4], kernal[4,2], kernal[4,4] = [2,2,2,2]
                kernal[1,1], kernal[1,2], kernal[1,3], kernal[1,4], kernal[1,5] = [1,1,1,1,1]
                kernal[5,1], kernal[5,2], kernal[5,3], kernal[5,4], kernal[5,5] = [1,1,1,1,1]
                kernal[2,1], kernal[3,1], kernal[4,1] = [1,1,1]
                kernal[2,5], kernal[3,5], kernal[4,5] = [1,1,1]
                kernal2 = kernal/18

                output = cv2.filter2D(img, -1, kernal1-kernal2)
            elif kernal == "7*7_Second":
                kernal = (np.ones((7,7), np.float32))
                kernal[3,3] = 8
                kernal1 = kernal/9

                kernal = (np.ones((7,7), np.float32))
                kernal[3,3] = 8
                kernal[3,2], kernal[3,4], kernal[2,3], kernal[4,3] = [4,4,4,4]
                kernal[2,2], kernal[2,4], kernal[4,2], kernal[4,4] = [2,2,2,2]
                kernal[1,1], kernal[1,2], kernal[1,3], kernal[1,4], kernal[1,5] = [1,1,1,1,1]
                kernal[5,1], kernal[5,2], kernal[5,3], kernal[5,4], kernal[5,5] = [1,1,1,1,1]
                kernal[2,1], kernal[3,1], kernal[4,1] = [1,1,1]
                kernal[2,5], kernal[3,5], kernal[4,5] = [1,1,1]
                kernal2 = kernal/6
                output = cv2.filter2D(img, -1, kernal2-kernal1)

            elif kernal == "9*9_First":
                kernal = (np.ones((9,9), np.float32))
                kernal[4,4] = 8
                kernal1 = kernal/9

                kernal = (np.ones((9,9), np.float32))
                kernal[4,4] = 16
                kernal[4,3], kernal[4,5], kernal[3,4], kernal[5,4] = [8,8,8,8]
                kernal[3,3], kernal[3,5], kernal[5,3], kernal[5,5] = [4,4,4,4]
                kernal[2,2], kernal[2,3], kernal[2,4], kernal[2,5], kernal[2,6] = [2,2,2,2,2]
                kernal[6,2], kernal[6,3], kernal[6,4], kernal[6,5], kernal[6,6] = [2,2,2,2,2]
                kernal[3,2], kernal[4,2], kernal[5,2] = [2,2,2]
                kernal[3,6], kernal[4,6], kernal[5,6] = [2,2,2]
                kernal[1,1], kernal[1,2], kernal[1,3], kernal[1,4], kernal[1,5], kernal[1,6], kernal[1,7] = [1,1,1,1,1,1,1]
                kernal[2,1], kernal[2,2], kernal[2,3], kernal[2,4], kernal[2,5], kernal[2,6], kernal[2,7] = [1,1,1,1,1,1,1]
                kernal[2,1], kernal[3,1], kernal[4,1], kernal[5,1], kernal[6,1] = [1,1,1,1,1]
                kernal[2,7], kernal[3,7], kernal[4,7], kernal[5,7], kernal[6,7] = [1,1,1,1,1]
                kernal2 = kernal/24

                output = cv2.filter2D(img, -1, kernal1-kernal2)
            elif kernal == "9*9_Second":
                kernal = (np.ones((9,9), np.float32))
                kernal[4,4] = 8
                kernal1 = kernal/9

                kernal = (np.ones((9,9), np.float32))
                kernal[4,4] = 16
                kernal[4,3], kernal[4,5], kernal[3,4], kernal[5,4] = [8,8,8,8]
                kernal[3,3], kernal[3,5], kernal[5,3], kernal[5,5] = [4,4,4,4]
                kernal[2,2], kernal[2,3], kernal[2,4], kernal[2,5], kernal[2,6] = [2,2,2,2,2]
                kernal[6,2], kernal[6,3], kernal[6,4], kernal[6,5], kernal[6,6] = [2,2,2,2,2]
                kernal[3,2], kernal[4,2], kernal[5,2] = [2,2,2]
                kernal[3,6], kernal[4,6], kernal[5,6] = [2,2,2]
                kernal[1,1], kernal[1,2], kernal[1,3], kernal[1,4], kernal[1,5], kernal[1,6], kernal[1,7] = [1,1,1,1,1,1,1]
                kernal[2,1], kernal[2,2], kernal[2,3], kernal[2,4], kernal[2,5], kernal[2,6], kernal[2,7] = [1,1,1,1,1,1,1]
                kernal[2,1], kernal[3,1], kernal[4,1], kernal[5,1], kernal[6,1] = [1,1,1,1,1]
                kernal[2,7], kernal[3,7], kernal[4,7], kernal[5,7], kernal[6,7] = [1,1,1,1,1]
                kernal2 = kernal/12               
                output = cv2.filter2D(img, -1, kernal2-kernal1)
            elif kernal == "11*11_First":
                kernal = 0 - ((np.ones((11,11), np.float32)))
                kernal[5,5] = 8
                kernal1 = kernal/9                
            
                kernal = 0 - (np.ones((11,11), np.float32))
                kernal[5,5] = 32
                kernal[5,4], kernal[5,6], kernal[4,5], kernal[6,5] = [16,16,16,16]
                kernal[4,4], kernal[4,6], kernal[6,4], kernal[6,6] = [8,8,8,8]
                kernal[3,3], kernal[3,4], kernal[3,5], kernal[3,6], kernal[3,7] = [4,4,4,4,4]
                kernal[7,3], kernal[7,4], kernal[7,5], kernal[7,6], kernal[7,7] = [4,4,4,4,4]
                kernal[6,3], kernal[4,3], kernal[5,3] = [4,4,4]
                kernal[6,7], kernal[4,7], kernal[5,7] = [4,4,4]
                kernal[2,2], kernal[2,3], kernal[2,4], kernal[2,5], kernal[2,6], kernal[2,7], kernal[2,8] = [2,2,2,2,2,2,2]
                kernal[8,2], kernal[8,3], kernal[8,4], kernal[8,5], kernal[8,6], kernal[8,7], kernal[8,8] = [2,2,2,2,2,2,2]
                kernal[3,2], kernal[4,2], kernal[5,2], kernal[6,2], kernal[7,2] = [2,2,2,2,2]
                kernal[2,8], kernal[3,8], kernal[4,8], kernal[5,8], kernal[6,8] = [2,2,2,2,2]
                kernal[1,1], kernal[1,2], kernal[1,3], kernal[1,4], kernal[1,5], kernal[1,6], kernal[1,7], kernal[1,8], kernal[1,9] = [1,1,1,1,1,1,1,1,1]
                kernal[9,1], kernal[9,2], kernal[9,3], kernal[9,4], kernal[9,5], kernal[9,6], kernal[9,7], kernal[9,8], kernal[9,9] = [1,1,1,1,1,1,1,1,1]
                kernal[2,1], kernal[3,1], kernal[4,1], kernal[5,1], kernal[6,1], kernal[7,1], kernal[8,1] = [1,1,1,1,1,1,1]
                kernal[2,9], kernal[3,9], kernal[4,9], kernal[5,9], kernal[6,9], kernal[7,9], kernal[8,9] = [1,1,1,1,1,1,1]                
                kernal2 = kernal/50
                output = cv2.filter2D(img, -1, kernal1-kernal2)
            
            else:
                kernal = 0 - ((np.ones((11,11), np.float32)))
                kernal[5,5] = 8
                kernal1 = kernal/9
                
            
                kernal = 0 - (np.ones((11,11), np.float32))
                kernal[5,5] = 32
                kernal[5,4], kernal[5,6], kernal[4,5], kernal[6,5] = [16,16,16,16]
                kernal[4,4], kernal[4,6], kernal[6,4], kernal[6,6] = [8,8,8,8]
                kernal[3,3], kernal[3,4], kernal[3,5], kernal[3,6], kernal[3,7] = [4,4,4,4,4]
                kernal[7,3], kernal[7,4], kernal[7,5], kernal[7,6], kernal[7,7] = [4,4,4,4,4]
                kernal[6,3], kernal[4,3], kernal[5,3] = [4,4,4]
                kernal[6,7], kernal[4,7], kernal[5,7] = [4,4,4]
                kernal[2,2], kernal[2,3], kernal[2,4], kernal[2,5], kernal[2,6], kernal[2,7], kernal[2,8] = [2,2,2,2,2,2,2]
                kernal[8,2], kernal[8,3], kernal[8,4], kernal[8,5], kernal[8,6], kernal[8,7], kernal[8,8] = [2,2,2,2,2,2,2]
                kernal[3,2], kernal[4,2], kernal[5,2], kernal[6,2], kernal[7,2] = [2,2,2,2,2]
                kernal[2,8], kernal[3,8], kernal[4,8], kernal[5,8], kernal[6,8] = [2,2,2,2,2]
                kernal[1,1], kernal[1,2], kernal[1,3], kernal[1,4], kernal[1,5], kernal[1,6], kernal[1,7], kernal[1,8], kernal[1,9] = [1,1,1,1,1,1,1,1,1]
                kernal[9,1], kernal[9,2], kernal[9,3], kernal[9,4], kernal[9,5], kernal[9,6], kernal[9,7], kernal[9,8], kernal[9,9] = [1,1,1,1,1,1,1,1,1]
                kernal[2,1], kernal[3,1], kernal[4,1], kernal[5,1], kernal[6,1], kernal[7,1], kernal[8,1] = [1,1,1,1,1,1,1]
                kernal[2,9], kernal[3,9], kernal[4,9], kernal[5,9], kernal[6,9], kernal[7,9], kernal[8,9] = [1,1,1,1,1,1,1]                
                kernal2 = kernal/24
                output = cv2.filter2D(img, -1, kernal2-kernal1)
        
        elif filter_type == 'NOTCH':
            if kernal == "3*3_First":
                kernal = (np.ones((3,3), np.float32))
                kernal[1,1] = 8
                kernal1 = kernal/9

                kernal = (np.ones((3,3), np.float32))
                kernal[1,1] = 4
                kernal[1,0], kernal[1,2], kernal[0,1], kernal[2,1] = [2,2,2,2]
                kernal2 = kernal/16

                kernal = (np.ones((3,3), np.float32))
                kernal[1,1] = 1

                output = cv2.filter2D(img, -1, kernal-(kernal1-kernal2))
            elif kernal == "3*3_Second":
                kernal = (np.ones((3,3), np.float32))
                kernal[1,1] = 8
                kernal1 = kernal/9

                kernal = (np.ones((3,3), np.float32))
                kernal[1,1] = 4
                kernal[1,0], kernal[1,2], kernal[0,1], kernal[2,1] = [2,2,2,2]
                kernal2 = kernal/3

                kernal = (np.ones((3,3), np.float32))
                kernal[1,1] = 1

                output = cv2.filter2D(img, -1, kernal-(kernal2-kernal1))
            elif kernal == "5*5_First":
                kernal = (np.ones((5,5), np.float32))
                kernal[2,2] = 8
                kernal1 = kernal/9

                kernal = (np.ones((5,5), np.float32))
                kernal[2,2] = 4
                kernal[1,2], kernal[3,2], kernal[2,1], kernal[2,3] = [2,2,2,2]
                kernal[1,1], kernal[1,3], kernal[3,1], kernal[3,3] = [1,1,1,1]
                kernal2 = kernal/16

                kernal = (np.ones((5,5), np.float32))
                kernal[2,2] = 1
                kernal = kernal/8

                output = cv2.filter2D(img, -1, kernal-(kernal1-kernal2))
            elif kernal == "5*5_Second":
                kernal = (np.ones((5,5), np.float32))
                kernal[2,2] = 8
                kernal1 = kernal/9

                kernal = (np.ones((5,5), np.float32))
                kernal[2,2] = 4
                kernal[1,2], kernal[3,2], kernal[2,1], kernal[2,3] = [2,2,2,2]
                kernal[1,1], kernal[1,3], kernal[3,1], kernal[3,3] = [1,1,1,1]
                kernal2 = kernal/3

                kernal = (np.ones((5,5), np.float32))
                kernal[2,2] = 1
                kernal = kernal/2

                output = cv2.filter2D(img, -1, kernal-(kernal2-kernal1))
            elif kernal == "7*7_First":
                kernal = (np.ones((7,7), np.float32))
                kernal[3,3] = 8
                kernal1 = kernal/9

                kernal = (np.ones((7,7), np.float32))
                kernal[3,3] = 8
                kernal[3,2], kernal[3,4], kernal[2,3], kernal[4,3] = [4,4,4,4]
                kernal[2,2], kernal[2,4], kernal[4,2], kernal[4,4] = [2,2,2,2]
                kernal[1,1], kernal[1,2], kernal[1,3], kernal[1,4], kernal[1,5] = [1,1,1,1,1]
                kernal[5,1], kernal[5,2], kernal[5,3], kernal[5,4], kernal[5,5] = [1,1,1,1,1]
                kernal[2,1], kernal[3,1], kernal[4,1] = [1,1,1]
                kernal[2,5], kernal[3,5], kernal[4,5] = [1,1,1]
                kernal2 = kernal/18

                kernal = (np.ones((7,7), np.float32))
                kernal[3,3] = 1
                kernal = kernal/12

                output = cv2.filter2D(img, -1, kernal-(kernal1-kernal2))
            elif kernal == "7*7_Second":
                kernal = (np.ones((7,7), np.float32))
                kernal[3,3] = 8
                kernal1 = kernal/9

                kernal = (np.ones((7,7), np.float32))
                kernal[3,3] = 8
                kernal[3,2], kernal[3,4], kernal[2,3], kernal[4,3] = [4,4,4,4]
                kernal[2,2], kernal[2,4], kernal[4,2], kernal[4,4] = [2,2,2,2]
                kernal[1,1], kernal[1,2], kernal[1,3], kernal[1,4], kernal[1,5] = [1,1,1,1,1]
                kernal[5,1], kernal[5,2], kernal[5,3], kernal[5,4], kernal[5,5] = [1,1,1,1,1]
                kernal[2,1], kernal[3,1], kernal[4,1] = [1,1,1]
                kernal[2,5], kernal[3,5], kernal[4,5] = [1,1,1]
                kernal2 = kernal/6

                kernal = (np.ones((7,7), np.float32))
                kernal[3,3] = 1
                kernal = kernal/6

                output = cv2.filter2D(img, -1, kernal-(kernal2-kernal1))

            elif kernal == "9*9_First":
                kernal = (np.ones((9,9), np.float32))
                kernal[4,4] = 8
                kernal1 = kernal/9

                kernal = (np.ones((9,9), np.float32))
                kernal[4,4] = 16
                kernal[4,3], kernal[4,5], kernal[3,4], kernal[5,4] = [8,8,8,8]
                kernal[3,3], kernal[3,5], kernal[5,3], kernal[5,5] = [4,4,4,4]
                kernal[2,2], kernal[2,3], kernal[2,4], kernal[2,5], kernal[2,6] = [2,2,2,2,2]
                kernal[6,2], kernal[6,3], kernal[6,4], kernal[6,5], kernal[6,6] = [2,2,2,2,2]
                kernal[3,2], kernal[4,2], kernal[5,2] = [2,2,2]
                kernal[3,6], kernal[4,6], kernal[5,6] = [2,2,2]
                kernal[1,1], kernal[1,2], kernal[1,3], kernal[1,4], kernal[1,5], kernal[1,6], kernal[1,7] = [1,1,1,1,1,1,1]
                kernal[2,1], kernal[2,2], kernal[2,3], kernal[2,4], kernal[2,5], kernal[2,6], kernal[2,7] = [1,1,1,1,1,1,1]
                kernal[2,1], kernal[3,1], kernal[4,1], kernal[5,1], kernal[6,1] = [1,1,1,1,1]
                kernal[2,7], kernal[3,7], kernal[4,7], kernal[5,7], kernal[6,7] = [1,1,1,1,1]
                kernal2 = kernal/24

                kernal = (np.ones((9,9), np.float32))
                kernal[4,4] = 1
                kernal = kernal/16

                output = cv2.filter2D(img, -1, kernal-(kernal1-kernal2))
            elif kernal == "9*9_second":
                kernal = (np.ones((9,9), np.float32))
                kernal[4,4] = 8
                kernal1 = kernal/9

                kernal = (np.ones((9,9), np.float32))
                kernal[4,4] = 16
                kernal[4,3], kernal[4,5], kernal[3,4], kernal[5,4] = [8,8,8,8]
                kernal[3,3], kernal[3,5], kernal[5,3], kernal[5,5] = [4,4,4,4]
                kernal[2,2], kernal[2,3], kernal[2,4], kernal[2,5], kernal[2,6] = [2,2,2,2,2]
                kernal[6,2], kernal[6,3], kernal[6,4], kernal[6,5], kernal[6,6] = [2,2,2,2,2]
                kernal[3,2], kernal[4,2], kernal[5,2] = [2,2,2]
                kernal[3,6], kernal[4,6], kernal[5,6] = [2,2,2]
                kernal[1,1], kernal[1,2], kernal[1,3], kernal[1,4], kernal[1,5], kernal[1,6], kernal[1,7] = [1,1,1,1,1,1,1]
                kernal[2,1], kernal[2,2], kernal[2,3], kernal[2,4], kernal[2,5], kernal[2,6], kernal[2,7] = [1,1,1,1,1,1,1]
                kernal[2,1], kernal[3,1], kernal[4,1], kernal[5,1], kernal[6,1] = [1,1,1,1,1]
                kernal[2,7], kernal[3,7], kernal[4,7], kernal[5,7], kernal[6,7] = [1,1,1,1,1]
                kernal2 = kernal/12 

                kernal = (np.ones((9,9), np.float32))
                kernal[4,4] = 1
                kernal = kernal/16

                output = cv2.filter2D(img, -1, kernal-(kernal2-kernal1))

            elif kernal == "11*11_First":
                kernal = 0 - ((np.ones((11,11), np.float32)))
                kernal[5,5] = 8
                kernal1 = kernal/9                
            
                kernal = 0 - (np.ones((11,11), np.float32))
                kernal[5,5] = 32
                kernal[5,4], kernal[5,6], kernal[4,5], kernal[6,5] = [16,16,16,16]
                kernal[4,4], kernal[4,6], kernal[6,4], kernal[6,6] = [8,8,8,8]
                kernal[3,3], kernal[3,4], kernal[3,5], kernal[3,6], kernal[3,7] = [4,4,4,4,4]
                kernal[7,3], kernal[7,4], kernal[7,5], kernal[7,6], kernal[7,7] = [4,4,4,4,4]
                kernal[6,3], kernal[4,3], kernal[5,3] = [4,4,4]
                kernal[6,7], kernal[4,7], kernal[5,7] = [4,4,4]
                kernal[2,2], kernal[2,3], kernal[2,4], kernal[2,5], kernal[2,6], kernal[2,7], kernal[2,8] = [2,2,2,2,2,2,2]
                kernal[8,2], kernal[8,3], kernal[8,4], kernal[8,5], kernal[8,6], kernal[8,7], kernal[8,8] = [2,2,2,2,2,2,2]
                kernal[3,2], kernal[4,2], kernal[5,2], kernal[6,2], kernal[7,2] = [2,2,2,2,2]
                kernal[2,8], kernal[3,8], kernal[4,8], kernal[5,8], kernal[6,8] = [2,2,2,2,2]
                kernal[1,1], kernal[1,2], kernal[1,3], kernal[1,4], kernal[1,5], kernal[1,6], kernal[1,7], kernal[1,8], kernal[1,9] = [1,1,1,1,1,1,1,1,1]
                kernal[9,1], kernal[9,2], kernal[9,3], kernal[9,4], kernal[9,5], kernal[9,6], kernal[9,7], kernal[9,8], kernal[9,9] = [1,1,1,1,1,1,1,1,1]
                kernal[2,1], kernal[3,1], kernal[4,1], kernal[5,1], kernal[6,1], kernal[7,1], kernal[8,1] = [1,1,1,1,1,1,1]
                kernal[2,9], kernal[3,9], kernal[4,9], kernal[5,9], kernal[6,9], kernal[7,9], kernal[8,9] = [1,1,1,1,1,1,1]                
                kernal2 = kernal/50

                kernal = 0 - ((np.ones((11,11), np.float32)))
                kernal[5,5] = 1
                kernal1 = kernal/16   
                output = cv2.filter2D(img, -1, kernal - (kernal1-kernal2))
            
            else:
                kernal = 0 - ((np.ones((11,11), np.float32)))
                kernal[5,5] = 8
                kernal1 = kernal/9
                
            
                kernal = 0 - (np.ones((11,11), np.float32))
                kernal[5,5] = 32
                kernal[5,4], kernal[5,6], kernal[4,5], kernal[6,5] = [16,16,16,16]
                kernal[4,4], kernal[4,6], kernal[6,4], kernal[6,6] = [8,8,8,8]
                kernal[3,3], kernal[3,4], kernal[3,5], kernal[3,6], kernal[3,7] = [4,4,4,4,4]
                kernal[7,3], kernal[7,4], kernal[7,5], kernal[7,6], kernal[7,7] = [4,4,4,4,4]
                kernal[6,3], kernal[4,3], kernal[5,3] = [4,4,4]
                kernal[6,7], kernal[4,7], kernal[5,7] = [4,4,4]
                kernal[2,2], kernal[2,3], kernal[2,4], kernal[2,5], kernal[2,6], kernal[2,7], kernal[2,8] = [2,2,2,2,2,2,2]
                kernal[8,2], kernal[8,3], kernal[8,4], kernal[8,5], kernal[8,6], kernal[8,7], kernal[8,8] = [2,2,2,2,2,2,2]
                kernal[3,2], kernal[4,2], kernal[5,2], kernal[6,2], kernal[7,2] = [2,2,2,2,2]
                kernal[2,8], kernal[3,8], kernal[4,8], kernal[5,8], kernal[6,8] = [2,2,2,2,2]
                kernal[1,1], kernal[1,2], kernal[1,3], kernal[1,4], kernal[1,5], kernal[1,6], kernal[1,7], kernal[1,8], kernal[1,9] = [1,1,1,1,1,1,1,1,1]
                kernal[9,1], kernal[9,2], kernal[9,3], kernal[9,4], kernal[9,5], kernal[9,6], kernal[9,7], kernal[9,8], kernal[9,9] = [1,1,1,1,1,1,1,1,1]
                kernal[2,1], kernal[3,1], kernal[4,1], kernal[5,1], kernal[6,1], kernal[7,1], kernal[8,1] = [1,1,1,1,1,1,1]
                kernal[2,9], kernal[3,9], kernal[4,9], kernal[5,9], kernal[6,9], kernal[7,9], kernal[8,9] = [1,1,1,1,1,1,1]                
                kernal2 = kernal/24

                kernal = 0 - ((np.ones((11,11), np.float32)))
                kernal[5,5] = 1
                kernal1 = kernal/16 

                output = cv2.filter2D(img, -1, kernal - (kernal2-kernal1))

        else:
            output = img

        return output


    def addition(self, method_id, current_user):
        if current_user.email == admin_user:
            original = os.path.join(APP_ROOT, str(current_user.username) + '_original/')
            original_two = os.path.join(APP_ROOT, str(current_user.username) + '_original_two/')
            second = os.path.join(APP_ROOT, str(current_user.username) + '_second/')
            result = os.path.join(APP_ROOT, str(current_user.username) + '_result/')
            
            file_original = os.listdir(original)        
            file_id, file_extension = os.path.splitext(file_original[0]) #file_extension of uploaded image
            image_path = os.path.join(original, file_original[0]) #path of uploaded image 
            if os.path.isdir(result):
                shutil.rmtree(result)
                shutil.rmtree(original_two)
                shutil.rmtree(second)                       
                os.mkdir(result)
                os.mkdir(original_two)
                os.mkdir(second)            
            else:    
                os.mkdir(result)
                os.mkdir(original_two)
                os.mkdir(second)
        else:
            original = os.path.join(APP_ROOT, str(current_user.username) + '_original/')
            result = os.path.join(APP_ROOT, str(current_user.username) + '_result/')
            file_original = os.listdir(original)        
            file_id, file_extension = os.path.splitext(file_original[0]) #file_extension of uploaded image
            image_path = os.path.join(original, file_original[0]) #path of uploaded image 
            if os.path.isdir(result):
                shutil.rmtree(result)
                os.mkdir(result)
            else:    
                os.mkdir(result)   

        #file_second = os.listdir(second)
        #image_path_2 = os.path.join(second, file_second[0])  
        img = cv2.imread(image_path)
        img_2 = img

        method = Methods.query.filter_by(method_id=method_id).first()   
        
        new_img = np.zeros(img.shape, img.dtype)
        new_img_2 = new_img
        new_add = new_img
        
        original_alpha = method.original_contrast/50
        original_beta = method.original_brightness - 50
        original_saturation = method.original_intensity/50
        copy_alpha = method.copy_contrast/50
        copy_beta = method.copy_brightness - 50
        copy_saturation = method.copy_intensity/50
        result_alpha = method.result_contrast/50
        result_beta = method.result_brightness - 50
        result_saturation = method.result_intensity/50
        original_filter = method.original_filter
        original_kernal = method.original_kernal
        copy_filter = method.copy_filter
        copy_kernal = method.copy_kernal    
        
        
        new_img = cv2.convertScaleAbs(img, alpha=original_alpha, beta=original_beta)
        hsvImg = cv2.cvtColor(new_img,cv2.COLOR_BGR2HSV)
        #multiple by a factor to change the saturation
        hsvImg[...,1] = hsvImg[...,1]*original_saturation
        new_img = cv2.cvtColor(hsvImg,cv2.COLOR_HSV2BGR)
        new_img = Image_processing().filter(new_img, original_filter, original_kernal)


        new_img_2 = cv2.convertScaleAbs(img, alpha=copy_alpha, beta=copy_beta)
        hsvImg = cv2.cvtColor(new_img_2,cv2.COLOR_BGR2HSV)
        #multiple by a factor to change the saturation
        hsvImg[...,1] = hsvImg[...,1]*copy_saturation
        new_img_2 = cv2.cvtColor(hsvImg,cv2.COLOR_HSV2BGR)
        new_img_2 = Image_processing().filter(new_img_2, copy_filter, copy_kernal)

        add = cv2.add(new_img,new_img_2)

        new_add = cv2.convertScaleAbs(add, alpha=result_alpha, beta=result_beta)
        hsvImg = cv2.cvtColor(new_add,cv2.COLOR_BGR2HSV)
        #multiple by a factor to change the saturation
        hsvImg[...,1] = hsvImg[...,1]*result_saturation
        new_add = cv2.cvtColor(hsvImg,cv2.COLOR_HSV2BGR)

        result_black_point = method.result_black_point
        result_midetone_slider = method.result_midetone_slider
        result_white_point = method.result_white_point

        new_add = Image_processing.LevelAdjustment(self,new_add, result_black_point, result_midetone_slider, result_white_point, current_user)

        filename_result = "Processed1" + str(random.randint(0,500)*random.randint(1001,1500)) + \
                    file_id + file_extension
        destination = "/".join([result, filename_result])
        b, g, r = cv2.split(new_add)
        new_add = cv2.merge((r,g,b))        
        im = Image.fromarray(new_add)
        im.save(destination)
        filename = [filename_result]


        if current_user.email == admin_user:
            original_black_point = method.original_black_point
            original_midetone_slider = method.original_midetone_slider
            original_white_point = method.original_white_point

            new_img = Image_processing.LevelAdjustment(self,new_img, original_black_point, original_midetone_slider, original_white_point, current_user)
            
            filename_original_two = "Processed1" + str(random.randint(501,1000)*random.randint(0,500)) + \
                        file_id + file_extension
            destination = "/".join([original_two, filename_original_two])
            b, g, r = cv2.split(new_img)
            new_img = cv2.merge((r,g,b))        
            im = Image.fromarray(new_img)
            im.save(destination)

            copy_black_point = method.copy_black_point
            copy_midetone_slider = method.copy_midetone_slider
            copy_white_point = method.copy_white_point

            new_img_2 = Image_processing.LevelAdjustment(self,new_img_2, copy_black_point, copy_midetone_slider, copy_white_point, current_user) 

            filename_second = "Processed1" + str(random.randint(1001,1500)*random.randint(501,1000)) + \
                        file_id + file_extension
            destination = "/".join([second, filename_second])
            b, g, r = cv2.split(new_img_2)
            new_img_2 = cv2.merge((r,g,b))        
            im = Image.fromarray(new_img_2)
            im.save(destination)
            filename = [filename_original_two, filename_second, filename_result]         
        
        return filename

    def subtraction(self, method_id, current_user):
        if current_user.email == admin_user:
            original = os.path.join(APP_ROOT, str(current_user.username) + '_original/')
            original_two = os.path.join(APP_ROOT, str(current_user.username) + '_original_two/')
            second = os.path.join(APP_ROOT, str(current_user.username) + '_second/')
            result = os.path.join(APP_ROOT, str(current_user.username) + '_result/')
            
            file_original = os.listdir(original)        
            file_id, file_extension = os.path.splitext(file_original[0]) #file_extension of uploaded image
            image_path = os.path.join(original, file_original[0]) #path of uploaded image 
            if os.path.isdir(result):
                shutil.rmtree(result)
                shutil.rmtree(original_two)
                shutil.rmtree(second)                       
                os.mkdir(result)
                os.mkdir(original_two)
                os.mkdir(second)            
            else:    
                os.mkdir(result)
                os.mkdir(original_two)
                os.mkdir(second)
        else:
            original = os.path.join(APP_ROOT, str(current_user.username) + '_original/')
            result = os.path.join(APP_ROOT, str(current_user.username) + '_result/')
            file_original = os.listdir(original)        
            file_id, file_extension = os.path.splitext(file_original[0]) #file_extension of uploaded image
            image_path = os.path.join(original, file_original[0]) #path of uploaded image 
            if os.path.isdir(result):
                shutil.rmtree(result)
                os.mkdir(result)
            else:    
                os.mkdir(result)            

        #file_second = os.listdir(second)
        #image_path_2 = os.path.join(second, file_second[0])  
        img = cv2.imread(image_path)
        img_2 = img

        method = Methods.query.filter_by(method_id=method_id).first()     
        
        
        new_img = np.zeros(img.shape, img.dtype)
        new_img_2 = new_img
        new_add = new_img
       
        
        
        original_alpha = method.original_contrast/50
        original_beta = method.original_brightness - 50
        original_saturation = method.original_intensity/50
        copy_alpha = method.copy_contrast/50
        copy_beta = method.copy_brightness - 50
        copy_saturation = method.copy_intensity/50
        result_alpha = method.result_contrast/50
        result_beta = method.result_brightness - 50
        result_saturation = method.result_intensity/50
        original_filter = method.original_filter
        original_kernal = method.original_kernal
        copy_filter = method.copy_filter
        copy_kernal = method.copy_kernal  
        '''for y in range(img.shape[0]):
            for x in range(img.shape[1]):
                for c in range(img.shape[1]):
                    new_img[y,x,c] = np.clip(original_alpha*img[y,x,c] + original_beta, 0, 255)
                    #new_img_2[y,x,c] = np.clip(copy_alpha*img[y,x,c] + copy_beta, 0, 255)'''

        new_img = cv2.convertScaleAbs(img, alpha=original_alpha, beta=original_beta)
        hsvImg = cv2.cvtColor(new_img,cv2.COLOR_BGR2HSV)
        #multiple by a factor to change the saturation
        hsvImg[...,1] = hsvImg[...,1]*original_saturation
        new_img = cv2.cvtColor(hsvImg,cv2.COLOR_HSV2BGR)
        new_img = Image_processing().filter(new_img, original_filter, original_kernal)

        '''for y in range(img.shape[0]):
            for x in range(img.shape[1]):
                for c in range(img.shape[2]):
                    new_img_2[y,x,c] = np.clip(copy_alpha*img_2[y,x,c] + copy_beta, 0, 255)'''

        new_img_2 = cv2.convertScaleAbs(img, alpha=copy_alpha, beta=copy_beta)
        hsvImg = cv2.cvtColor(new_img_2,cv2.COLOR_BGR2HSV)
        #multiple by a factor to change the saturation
        hsvImg[...,1] = hsvImg[...,1]*copy_saturation
        new_img_2 = cv2.cvtColor(hsvImg,cv2.COLOR_HSV2BGR)
        new_img_2 = Image_processing().filter(new_img_2, copy_filter, copy_kernal)

        sub = new_img - new_img_2
        '''for y in range(sub.shape[0]):
            for x in range(sub.shape[1]):
                for c in range(sub.shape[2]):
                    new_sub[y,x,c] = np.clip(result_alpha*sub[y,x,c] + result_beta, 0, 255)'''

        new_sub = cv2.convertScaleAbs(sub, alpha=result_alpha, beta=result_beta)
        hsvImg = cv2.cvtColor(new_sub,cv2.COLOR_BGR2HSV)
        #multiple by a factor to change the saturation
        hsvImg[...,1] = hsvImg[...,1]*result_saturation
        new_sub = cv2.cvtColor(hsvImg,cv2.COLOR_HSV2BGR)

        result_black_point = method.result_black_point
        result_midetone_slider = method.result_midetone_slider
        result_white_point = method.result_white_point

        new_sub = Image_processing.LevelAdjustment(self,new_sub, result_black_point, result_midetone_slider, result_white_point, current_user)

        filename_result = "Processed1" + str(random.randint(0,500)*random.randint(1001,1500)) + \
                    file_id + file_extension
        destination = "/".join([result, filename_result])
        b, g, r = cv2.split(new_sub)
        new_sub = cv2.merge((r,g,b))        
        im = Image.fromarray(new_sub)
        im.save(destination)
        filename = [filename_result]


        if current_user.email == admin_user:
            original_black_point = method.original_black_point
            original_midetone_slider = method.original_midetone_slider
            original_white_point = method.original_white_point

            new_img = Image_processing.LevelAdjustment(self,new_img, original_black_point, original_midetone_slider, original_white_point, current_user)
            
            filename_original_two = "Processed1" + str(random.randint(501,1000)*random.randint(0,500)) + \
                        file_id + file_extension
            destination = "/".join([original_two, filename_original_two])
            b, g, r = cv2.split(new_img)
            new_img = cv2.merge((r,g,b))        
            im = Image.fromarray(new_img)
            im.save(destination)

            copy_black_point = method.copy_black_point
            copy_midetone_slider = method.copy_midetone_slider
            copy_white_point = method.copy_white_point

            new_img_2 = Image_processing.LevelAdjustment(self,new_img_2, copy_black_point, copy_midetone_slider, copy_white_point, current_user) 

            filename_second = "Processed1" + str(random.randint(1001,1500)*random.randint(501,1000)) + \
                        file_id + file_extension
            destination = "/".join([second, filename_second])
            b, g, r = cv2.split(new_img_2)
            new_img_2 = cv2.merge((r,g,b))        
            im = Image.fromarray(new_img_2)
            im.save(destination)
            filename = [filename_original_two, filename_second, filename_result]         
        
        return filename

    def multiplication(self, method_id, current_user):
        if current_user.email == admin_user:
            original = os.path.join(APP_ROOT, str(current_user.username) + '_original/')
            original_two = os.path.join(APP_ROOT, str(current_user.username) + '_original_two/')
            second = os.path.join(APP_ROOT, str(current_user.username) + '_second/')
            result = os.path.join(APP_ROOT, str(current_user.username) + '_result/')
            
            file_original = os.listdir(original)        
            file_id, file_extension = os.path.splitext(file_original[0]) #file_extension of uploaded image
            image_path = os.path.join(original, file_original[0]) #path of uploaded image 
            if os.path.isdir(result):
                shutil.rmtree(result)
                shutil.rmtree(original_two)
                shutil.rmtree(second)                       
                os.mkdir(result)
                os.mkdir(original_two)
                os.mkdir(second)            
            else:    
                os.mkdir(result)
                os.mkdir(original_two)
                os.mkdir(second)
        else:
            original = os.path.join(APP_ROOT, str(current_user.username) + '_original/')
            result = os.path.join(APP_ROOT, str(current_user.username) + '_result/')
            file_original = os.listdir(original)        
            file_id, file_extension = os.path.splitext(file_original[0]) #file_extension of uploaded image
            image_path = os.path.join(original, file_original[0]) #path of uploaded image 
            if os.path.isdir(result):
                shutil.rmtree(result)
                os.mkdir(result)
            else:    
                os.mkdir(result)          

        #file_second = os.listdir(second)
        #image_path_2 = os.path.join(second, file_second[0])  
        img = cv2.imread(image_path)
        img_2 = img

        method = Methods.query.filter_by(method_id=method_id).first()     
        
        
        new_img = np.zeros(img.shape, img.dtype)
        new_img_2 = new_img
        new_add = new_img
       
        alpha = 1.0 # Simple contrast control
        beta = 0    # Simple brightness control
        
        original_alpha = method.original_contrast/50
        original_beta = method.original_brightness - 50
        original_saturation = method.original_intensity/50
        copy_alpha = method.copy_contrast/50
        copy_beta = method.copy_brightness - 50
        copy_saturation = method.copy_intensity/50
        result_alpha = method.result_contrast/50
        result_beta = method.result_brightness - 50
        result_saturation = method.result_intensity/50
        original_filter = method.original_filter
        original_kernal = method.original_kernal
        copy_filter = method.copy_filter
        copy_kernal = method.copy_kernal 
        '''for y in range(img.shape[0]):
            for x in range(img.shape[1]):
                for c in range(img.shape[2]):
                    new_img[y,x,c] = np.clip(original_alpha*img[y,x,c] + original_beta, 0, 255)
                    #new_img_2[y,x,c] = np.clip(copy_alpha*img[y,x,c] + copy_beta, 0, 255)'''

        new_img = cv2.convertScaleAbs(img, alpha=original_alpha, beta=original_beta)
        hsvImg = cv2.cvtColor(new_img,cv2.COLOR_BGR2HSV)
        #multiple by a factor to change the saturation
        hsvImg[...,1] = hsvImg[...,1]*original_saturation
        new_img = cv2.cvtColor(hsvImg,cv2.COLOR_HSV2BGR)
        new_img = Image_processing().filter(new_img, original_filter, original_kernal)

        '''for y in range(img.shape[0]):
            for x in range(img.shape[1]):
                for c in range(img.shape[2]):
                    new_img_2[y,x,c] = np.clip(copy_alpha*img_2[y,x,c] + copy_beta, 0, 255)'''

        new_img_2 = cv2.convertScaleAbs(img, alpha=copy_alpha, beta=copy_beta)
        hsvImg = cv2.cvtColor(new_img_2,cv2.COLOR_BGR2HSV)
        #multiple by a factor to change the saturation
        hsvImg[...,1] = hsvImg[...,1]*original_saturation
        new_img_2 = cv2.cvtColor(hsvImg,cv2.COLOR_HSV2BGR)
        new_img_2 = Image_processing().filter(new_img_2, copy_filter, copy_kernal)

        mul = np.multiply(new_img, new_img_2)
        '''for y in range(mul.shape[0]):
            for x in range(mul.shape[1]):
                for c in range(mul.shape[2]):
                    new_mul[y,x,c] = np.clip(result_alpha*mul[y,x,c] + result_beta, 0, 255)'''

        new_mul = cv2.convertScaleAbs(mul, alpha=result_alpha, beta=result_beta)
        hsvImg = cv2.cvtColor(new_mul,cv2.COLOR_BGR2HSV)
        #multiple by a factor to change the saturation
        hsvImg[...,1] = hsvImg[...,1]*original_saturation
        new_mul = cv2.cvtColor(hsvImg,cv2.COLOR_HSV2BGR)

        result_black_point = method.result_black_point
        result_midetone_slider = method.result_midetone_slider
        result_white_point = method.result_white_point

        new_mul = Image_processing.LevelAdjustment(self,new_mul, result_black_point, result_midetone_slider, result_white_point, current_user)

        filename_result = "Processed1" + str(random.randint(0,500)*random.randint(1001,1500)) + \
                    file_id + file_extension
        destination = "/".join([result, filename_result])
        b, g, r = cv2.split(new_mul)
        new_mul = cv2.merge((r,g,b))        
        im = Image.fromarray(new_mul)
        im.save(destination)
        filename = [filename_result]


        if current_user.email == admin_user:
            original_black_point = method.original_black_point
            original_midetone_slider = method.original_midetone_slider
            original_white_point = method.original_white_point

            new_img = Image_processing.LevelAdjustment(self,new_img, original_black_point, original_midetone_slider, original_white_point, current_user)
            
            filename_original_two = "Processed1" + str(random.randint(501,1000)*random.randint(0,500)) + \
                        file_id + file_extension
            destination = "/".join([original_two, filename_original_two])
            b, g, r = cv2.split(new_img)
            new_img = cv2.merge((r,g,b))        
            im = Image.fromarray(new_img)
            im.save(destination)

            copy_black_point = method.copy_black_point
            copy_midetone_slider = method.copy_midetone_slider
            copy_white_point = method.copy_white_point

            new_img_2 = Image_processing.LevelAdjustment(self,new_img_2, copy_black_point, copy_midetone_slider, copy_white_point, current_user) 

            filename_second = "Processed1" + str(random.randint(1001,1500)*random.randint(501,1000)) + \
                        file_id + file_extension
            destination = "/".join([second, filename_second])
            b, g, r = cv2.split(new_img_2)
            new_img_2 = cv2.merge((r,g,b))        
            im = Image.fromarray(new_img_2)
            im.save(destination)
            filename = [filename_original_two, filename_second, filename_result]         
        
        return filename

   
    def LevelAdjustment(self, img, black_point, midetone_slider, white_point, current_user):
        '''original = os.path.join(APP_ROOT, str(current_user.username) + '_original/')
        
        file_original = os.listdir(original)        
        file_id, file_extension = os.path.splitext(file_original[0]) #file_extension of uploaded image
        result = os.path.join(APP_ROOT, str(current_user.username) + '_result/')      
        #image_path = os.path.join(result, os.listdir(result)[0]) #path of uploaded image''' 
        image = img
        
        counter = 0
        pixel_to_match = 20

        for i in range(pixel_to_match):
            pixel = image[random.randint(0,image.shape[0]-1), random.randint(0, image.shape[1]-1)]
            if pixel[0] == pixel[1] and pixel[0] == pixel[2]:
                counter += 1
            else:
                break
        
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                pixels = image[i, j]
            
                if counter != pixel_to_match:
                    for color, pixel in enumerate(pixels) :
                        if pixel > white_point:
                            pixels[color] = 255
                        elif pixel < black_point:
                            pixels[color] = 0

                else:
                    if pixels[0] > white_point:
                        pixels[0] = 255
                        pixels[1] = 255
                        pixels[2] = 255
                    elif pixels[0] < black_point:
                        pixels[0] = 0
                        pixels[1] = 0
                        pixels[2] = 0


        
        gamma = midetone_slider if midetone_slider > 0 else 0.1
        # build a lookup table mapping the pixel values [0, 255] to
        # their adjusted gamma values
        invGamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")

        # apply gamma correction using the lookup table
        image = cv2.LUT(image, table)

        return image
        
        '''filename = Image_processing.LevelAdjustment.__name__ + str(random.randint(1001,1500)*random.randint(501,1000)) + \
                    file_id + file_extension
        destination = "/".join([result_histo, filename])
        b, g, r = cv2.split(image)
        image = cv2.merge((r,g,b))        
        im = Image.fromarray(image)
        im.save(destination)'''
        
        
        
        
            