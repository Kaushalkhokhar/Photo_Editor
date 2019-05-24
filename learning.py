import os, cv2
import numpy as np 


img = cv2.imread(r"D:\Programming\Python\Flask\Web_App\src\Sample Images\airplane.png")
img_2 = cv2.imread(r"D:\Programming\Python\Flask\Web_App\src\Sample Images\cameraman.png")

print(len(img_2[1].shape))

if np.all(img[2][:,0] == img[2][:,1]):
    print('gray')
else: 
    print("color")  