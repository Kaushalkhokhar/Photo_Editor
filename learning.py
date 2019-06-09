from __future__ import division
import cv2

import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('D:\Programming\Python\Flask\Web_App\src\web_app\sample_images\girl.png', 0)
f = np.fft.fft2(img)
print(np.amax(f))
print(np.amin(f))
fshift = np.fft.fftshift(f)
print(np.amax(fshift))
print(np.amin(fshift))

magnitude_spectrum = 20*np.log(np.abs(fshift))

plt.subplot(121),plt.imshow(img, cmap = 'gray')
plt.title('Input Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(magnitude_spectrum, cmap = 'gray')
plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
#plt.show()