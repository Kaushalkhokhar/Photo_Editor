import os, shutil, cv2, random
from PIL import Image
import numpy as np
from web_app import original, second, result, original_two
from web_app.model import Methods

class Image_processing():
    def __init__(self):        
        '''self.APP_ROOT = os.path.dirname(os.path.abspath(__file__)) 
        self.processed_image = os.path.join(self.APP_ROOT, 'processed_images/') #To store processed image        

        self.file_original = os.listdir(os.path.join(self.APP_ROOT, 'Original/'))
        self.file_second = os.listdir(os.path.join(self.APP_ROOT, 'Second/'))

        self.file_id, self.file_extension = os.path.splitext(self.file_original[0]) #self.file_extension of uploaded image
        self.image_path = os.path.join(self.APP_ROOT, 'Original/', self.file_original[0]) #path of uploaded image  
        self.image_path_2 = os.path.join(self.APP_ROOT, 'Second/', self.file_second[0])'''      
        
        self.file_original = os.listdir(original)        
        self.file_id, self.file_extension = os.path.splitext(self.file_original[0]) #self.file_extension of uploaded image
        self.image_path = os.path.join(original, self.file_original[0]) #path of uploaded image  
            

    def convolution(self):           
        img = cv2.imread(self.image_path)
        '''if len(img.shape) == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)''' #To convert color iamge to gray scale 
        
        kernel = np.ones((5,5),np.float32)/25
        dst = cv2.filter2D(img,-1,kernel)

        filename = image_operations.convolution.__name__ + self.file_id + self.file_extension
        destination = "/".join([result, filename])        
        im = Image.fromarray(dst)
        im.save(destination)

        return filename   

    def averaging(self):   
        img = cv2.imread(self.image_path)
        '''if len(img.shape) == 3:  
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)'''
        blur = cv2.blur(img,(5,5))

        filename = image_operations.averaging.__name__ + self.file_id + self.file_extension
        destination = "/".join([result, filename])        
        im = Image.fromarray(blur)
        im.save(destination)        

        return filename    

    def gaussian_blur(self):    
        img = cv2.imread(self.image_path)
        '''if len(img.shape) == 3: 
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)'''
        blur = cv2.GaussianBlur(img,(5,5),0)

        filename = image_operations.gaussian_blur.__name__ + self.file_id + self.file_extension
        destination = "/".join([result, filename])        
        im = Image.fromarray(blur)
        im.save(destination)

        return filename   

    def median_blur(self):    
        img = cv2.imread(self.image_path)
        '''if len(img.shape) == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)'''
        blur = cv2.medianBlur(img,5)

        filename = image_operations.median_blur.__name__ + self.file_id + self.file_extension
        destination = "/".join([result, filename])        
        im = Image.fromarray(blur)
        im.save(destination)

        return filename 

    def bilateral_blur(self):   
        img = cv2.imread(self.image_path)
        '''if len(img.shape) == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)'''
        blur = cv2.bilateralFilter(img,9,75,75)

        filename = image_operations.bilateral_blur.__name__ + self.file_id + self.file_extension
        destination = "/".join([result, filename])        
        im = Image.fromarray(blur)
        im.save(destination)

        return filename

    def addition(self, method_id):
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

        file_second = os.listdir(second)
        #image_path_2 = os.path.join(second, file_second[0])  
        img = cv2.imread(self.image_path)
        img_2 = img

        method = Methods.query.filter_by(method_id=method_id).first()     
        
        
        new_img = np.zeros(img.shape, img.dtype)
        new_img_2 = new_img
        new_add = new_img
       
        alpha = 1.0 # Simple contrast control
        beta = 0    # Simple brightness control
        '''original_alpha = (1 + (method.original_contrast * 0.02 ))
        original_beta = method.original_brightness
        copy_alpha = (1 + (method.copy_contrast * 0.02))
        copy_beta = method.copy_brightness
        result_alpha = (1 + (method.result_contrast * 0.02))
        result_beta = method.result_brightness'''
        original_alpha = method.original_contrast/50
        original_beta = method.original_brightness - 50
        copy_alpha = method.copy_contrast/50
        copy_beta = method.copy_brightness - 50
        result_alpha = method.result_contrast/50
        result_beta = method.result_brightness - 50  
        '''for y in range(img.shape[0]):
            for x in range(img.shape[1]):
                for c in range(img.shape[2]):
                    new_img[y,x,c] = np.clip(original_alpha*img[y,x,c] + original_beta, 0, 255)
                    #new_img_2[y,x,c] = np.clip(copy_alpha*img[y,x,c] + copy_beta, 0, 255)'''

        new_img = cv2.convertScaleAbs(img, alpha=original_alpha, beta=original_beta)

        '''for y in range(img.shape[0]):
            for x in range(img.shape[1]):
                for c in range(img.shape[2]):
                    new_img_2[y,x,c] = np.clip(copy_alpha*img_2[y,x,c] + copy_beta, 0, 255)'''

        new_img_2 = cv2.convertScaleAbs(img, alpha=copy_alpha, beta=copy_beta)

        add = cv2.add(new_img,new_img_2)
        '''for y in range(add.shape[0]):
            for x in range(add.shape[1]):
                for c in range(add.shape[2]):
                    new_add[y,x,c] = np.clip(result_alpha*add[y,x,c] + result_beta, 0, 255)'''

        new_add = cv2.convertScaleAbs(add, alpha=result_alpha, beta=result_beta)


        filename_result = Image_processing.addition.__name__ + str(random.randint(0,500)*random.randint(1001,1500)) + \
                    self.file_id + self.file_extension
        destination = "/".join([result, filename_result])        
        im = Image.fromarray(new_add)
        im.save(destination)

        filename_original_two = Image_processing.addition.__name__ + str(random.randint(501,1000)*random.randint(0,500)) + \
                    self.file_id + self.file_extension
        destination = "/".join([original_two, filename_original_two])        
        im = Image.fromarray(new_img)
        im.save(destination) 

        filename_second = Image_processing.addition.__name__ + str(random.randint(1001,1500)*random.randint(501,1000)) + \
                    self.file_id + self.file_extension
        destination = "/".join([second, filename_second])        
        im = Image.fromarray(new_img_2)
        im.save(destination)         
        
        return filename_original_two, filename_second, filename_result

    def substraction(self, method):
        if os.path.isdir(result):
            shutil.rmtree(result)            
            os.mkdir(result)
        else:    
            os.mkdir(result)

        file_second = os.listdir(second)
        image_path_2 = os.path.join(second, file_second[0])  
        img = cv2.imread(self.image_path)
        img_2 = cv2.imread(image_path_2)
        

        sub = img - img_2        
        filename = image_operations.substraction.__name__ + self.file_id + self.file_extension
        destination = "/".join([result, filename])        
        im = Image.fromarray(sub)
        im.save(destination)        
        
        return filename

    def multiplication(self, method):
        if os.path.isdir(result):
            shutil.rmtree(result)            
            os.mkdir(result)
        else:    
            os.mkdir(result)
            
        file_second = os.listdir(second)
        image_path_2 = os.path.join(second, file_second[0])  
        img = cv2.imread(self.image_path)
        img_2 = cv2.imread(image_path_2)        

        mul = cv2.multiply(img, img_2)       
        filename = image_operations.multiplication.__name__ + self.file_id + self.file_extension
        destination = "/".join([result, filename])        
        im = Image.fromarray(mul)
        im.save(destination)        
        
        return filename
        
        
        
        
            