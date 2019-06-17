import cv2, os
from PIL import Image
 
img = cv2.imread(r'D:\Programming\Python\Flask\Web_App\src\web_app\sample_images\Admin_Settings.png', cv2.IMREAD_UNCHANGED)
 
print('Original Dimensions : ',img.shape)
 
scale_percent = 70 # percent of original size
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * 90 / 100)
dim = (width, height)
# resize image
resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

filename_result = "resize_50.png"
destination = "/".join([os.path.dirname(os.path.abspath(__file__)), filename_result])
b, g, r = cv2.split(resized)
new_add = cv2.merge((r,g,b))        
im = Image.fromarray(new_add)
im.save(destination)