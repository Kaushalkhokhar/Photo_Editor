import os, shutil, cv2
import numpy as np
import random
import matplotlib.pyplot as plt
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource
from bokeh.models.glyphs import VBar
from bokeh.embed import components
from bokeh.palettes import Spectral6, Magma
from bokeh.transform import linear_cmap
from web_app import APP_ROOT


class Spectograph():    
    def __init__(self):            
       pass
            
    def spectograph_plot(self, current_user):
        original = os.path.join(APP_ROOT, str(current_user.username) + '_original/')        
        result = os.path.join(APP_ROOT, str(current_user.username) + '_result/')
        result_specto = os.path.join(APP_ROOT, str(current_user.username) + '_result_specto/')

        if os.path.isdir(result_specto):
            shutil.rmtree(result_specto)
            os.mkdir(result_specto)
        else:    
            os.mkdir(result_specto)

        if os.listdir(result):
            image  = cv2.imread(os.path.join(result, os.listdir(result)[0]), cv2.IMREAD_COLOR)
        else:
            image = cv2.imread(os.path.join(original, os.listdir(original)[0]), cv2.IMREAD_COLOR)
        
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)   
        
        # 0th elemwnt is teh hue
        h = image[:,:,0]

        # Intensity is the average of all the three elements
        temp = np.array(image)
        I = (temp[:,:,1] + temp[:,:,2] + temp[:,:,0])/(255)

        # This is the variable to multiply with the matrix.
        mul = ((470-700)/120)
        L = np.array(h)
        L =  mul * L + 700

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

        barlist=plt.bar(u_wavelength, max_intensity)
        for i , wave_len in enumerate(u_wavelength):
            RGBcolors = Spectograph().wavelength_to_rgb(int(wave_len))
            barlist[i].set_color(RGBcolors)

        # Add title and axis names
        plt.title('Spectrum of the Colors')
        plt.xlabel('Wavelength')
        plt.ylabel('Intensity')
        #plt.show()

        destination = "/".join([result_specto, 'result_specto' + str(random.randint(0,500)*random.randint(1001,1500)) + '.png'])
        plt.savefig(destination)
        
        # for parsing array to bokeh
        mapper = linear_cmap(field_name='x1', palette=Spectral6 ,low=min(u_wavelength) ,high=max(u_wavelength))
        #mapper = linear_cmap(field_name='x1', palette=Magma ,low=min(u_wavelength) ,high=max(u_wavelength))

        #To merge data x and y and added to glyphs
        source = ColumnDataSource(dict(x1=u_wavelength, 
                                    y1=max_intensity,
                                    ))

        #To design layout of figure '''plot_width=1000, plot_height=500,'''
        plot = figure(
            title='Spectograph of Image', plot_width=600, plot_height=400,
            min_border=0, toolbar_location='right') # toolbar_location can be edited to change logo 

        #Creating and adding glyph to plot
        glyph_y1 = VBar(x="x1", top="y1", bottom=0, width=1, fill_alpha=1, fill_color=mapper)
        plot.add_glyph(source, glyph_y1)
        
        # Separating Script and div
        script, div = components(plot)

        return script, div
   
    def wavelength_to_rgb(self,wavelength, gamma=0.8):

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

    