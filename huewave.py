import numpy as np
import matplotlib.pyplot as plt
import cv2
import random
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource
from bokeh.models.glyphs import VBar
from bokeh.embed import components
from bokeh.palettes import Spectral6
from bokeh.transform import linear_cmap
def wavelength_to_rgb(wavelength, gamma=0.8):

    '''This converts a given wavelength of light to an
    approximate RGB color value. The wavelength must be given
    in nanometers in the range from 380 nm through 750 nm
    (789 THz through 400 THz).

    Based on code by Dan Bruton
    http://www.physics.sfasu.edu/astro/color/spectra.html
    '''

    wavelength = float(wavelength)
    if wavelength >= 380 and wavelength <= 440:
        attenuation = 0.3 + 0.7 * (wavelength - 380) / (440 - 380)
        R = ((-(wavelength - 440) / (440 - 380)) * attenuation) ** gamma
        G = 0.0
        B = (1.0 * attenuation) ** gamma
    elif wavelength >= 440 and wavelength <= 490:
        R = 0.0
        G = ((wavelength - 440) / (490 - 440)) ** gamma
        B = 1.0
    elif wavelength >= 490 and wavelength <= 510:
        R = 0.0
        G = 1.0
        B = (-(wavelength - 510) / (510 - 490)) ** gamma
    elif wavelength >= 510 and wavelength <= 580:
        R = ((wavelength - 510) / (580 - 510)) ** gamma
        G = 1.0
        B = 0.0
    elif wavelength >= 580 and wavelength <= 645:
        R = 1.0
        G = (-(wavelength - 645) / (645 - 580)) ** gamma
        B = 0.0
    elif wavelength >= 645 and wavelength <= 750:
        attenuation = 0.3 + 0.7 * (750 - wavelength) / (750 - 645)
        R = (1.0 * attenuation) ** gamma
        G = 0.0
        B = 0.0
    else:
        R = 0.0
        G = 0.0
        B = 0.0
    R *= 1
    G *= 1
    B *= 1
    return (R, G, B)

if __name__ == "__main__":
    image = cv2.imread(r'D:\Programming\Python\Flask\Web_App\src\web_app\sample_images\girl.png')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)   
    plt.imshow(image)
    plt.show()

    # 0th elemwnt is teh hue
    h = image[:,:,0]

    # Intensity is the average of all the three elements
    temp = np.array(image)
    I = (temp[:,:,1] + temp[:,:,2] + temp[:,:,0])/(255)

    # This is the variable to multiply with the matrix.
    mul = ((750-380)/270)
    L = np.array(h)
    L =  mul * L + 380

    # reshape and sort the wavelength to plot the graph
    temp_L = np.reshape(L,L.shape[0]*L.shape[1])
    sort_L = sorted(temp_L)
    index_sort_L = np.argsort(temp_L)

    temp_I = np.reshape(I, I.shape[0]*I.shape[1])
    sort_I = temp_I[index_sort_L] 

    # This is to findout the unique and maximum Intensity for the given 
    # value of the wavelength{}
    u_wavelength = np.unique(sort_L)
    max_intensity = []
    for i in u_wavelength:
        itemindex = np.where(sort_L==i)
        #maxintensity = max(sort_I[itemindex])
        maxintensity = np.mean(sort_I[itemindex])

        max_intensity.append(maxintensity)

    print(max_intensity)

    '''barlist=plt.bar(u_wavelength, max_intensity)
    for i , wave_len in enumerate(u_wavelength):
        RGBcolors = wavelength_to_rgb(int(wave_len))
        barlist[i].set_color(RGBcolors)

    print(max_intensity)

    # Add title and axis names
    plt.title('Specturm of the Colors')
    plt.xlabel('Wavelength')
    plt.ylabel('Intensity')
    plt.show()'''

    mapper = linear_cmap(field_name='x1', palette=Spectral6 ,low=min(u_wavelength) ,high=max(u_wavelength))

    #To merge data x and y and added to glyphs
    source = ColumnDataSource(dict(x1=u_wavelength, 
                                b_hist=max_intensity,
                                ))

    #To design layout of figure '''plot_width=1000, plot_height=500,'''
    plot = figure(
        title='Spectograph of Image', plot_width=700, plot_height=400,
        min_border=0, toolbar_location='right') # toolbar_location can be edited to change logo 

    

    #Creating and adding glyph to plot
    glyph_b = VBar(x="x1", top="b_hist", bottom=0, width=1, fill_alpha=1, fill_color=mapper)
    # glyph_g = VBar(x="x2", top="g_hist", bottom=0, width=0.5, fill_alpha=0.8, fill_color="green")
    # glyph_r = VBar(x="x3", top="r_hist", bottom=0, width=0.5, fill_alpha=0.8, fill_color="red")
    plot.add_glyph(source, glyph_b)
    # plot.add_glyph(source, glyph_g)
    # plot.add_glyph(source, glyph_r)

    #script, div = components(plot)   

    #return script, div
    
    show(plot)