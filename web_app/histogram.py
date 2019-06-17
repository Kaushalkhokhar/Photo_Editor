import os, shutil, cv2
import numpy as np
import random
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource
from bokeh.models.glyphs import VBar
from bokeh.embed import components
from bokeh.palettes import Spectral6
from bokeh.transform import linear_cmap
from web_app import APP_ROOT








class Histogram():    
    def __init__(self):            
        '''file_processed = []
        for (dirpath, dirnames, filenames) in os.walk(os.path.join(APP_ROOT, 'processed_images/')):
            file_processed.extend(filenames)'''
        
        #file_processed = os.listdir(result)
        
        '''file_source = []
        for (dirpath, dirnames, filenames) in os.walk(os.path.join(APP_ROOT, 'Original/')):
            file_source.extend(filenames)'''

        #file_source = os.listdir(original)

        #self.processed_image_path = os.path.join(result, file_processed[0])

            
    def histogram_plot(self, current_user):
        original = os.path.join(APP_ROOT, str(current_user.username) + '_original/')        
        result = os.path.join(APP_ROOT, str(current_user.username) + '_result/')

        if os.listdir(result):
            image  = cv2.imread(os.path.join(result, os.listdir(result)[0]), cv2.IMREAD_COLOR)
        else:
            image = cv2.imread(os.path.join(original, os.listdir(original)[0]), cv2.IMREAD_COLOR)
              

        histSize = 256 #no of bins
        
        #To decide x value for histogram. we have separated using some decimal value
        x_1 = np.linspace(0, 255, histSize) 
        x_2 = np.linspace(0.2, 255.2, histSize)
        x_3 = np.linspace(0.4, 255.4, histSize)
        hist_h = 250

        bgr_plane = cv2.split(image) #To split bgr_plane
        histRange = (0, 256) # the upper boundary is exclusive
        accumulate = False # to have histpgram of same size

        #To calculate hiisogram value of each color from range o to 256
        b_hist = cv2.calcHist(bgr_plane, [0], None, [histSize], histRange, accumulate=accumulate)
        g_hist = cv2.calcHist(bgr_plane, [1], None, [histSize], histRange, accumulate=accumulate)
        r_hist = cv2.calcHist(bgr_plane, [2], None, [histSize], histRange, accumulate=accumulate)
        
        #To normlize data
        b_hist = cv2.normalize(b_hist, b_hist, alpha=0, beta=hist_h, norm_type=cv2.NORM_MINMAX).astype(int).flatten()
        g_hist = cv2.normalize(g_hist, g_hist, alpha=0, beta=hist_h, norm_type=cv2.NORM_MINMAX).astype(int).flatten()
        r_hist = cv2.normalize(r_hist, r_hist, alpha=0, beta=hist_h, norm_type=cv2.NORM_MINMAX).astype(int).flatten()

        #To merge data x and y and added to glyphs
        source = ColumnDataSource(dict(x1=x_1, b_hist=b_hist,
                                    x2=x_2, g_hist=g_hist,
                                    x3=x_3, r_hist=r_hist,))

        #To design layout of figure '''plot_width=1000, plot_height=500,'''
        plot = figure(
            title='Histogram of Image', plot_width=1200, plot_height=400,
            min_border=0, toolbar_location='right') # toolbar_location can be edited to change logo 

        #Creating and adding glyph to plot
        glyph_b = VBar(x="x1", top="b_hist", bottom=0, width=0.5, fill_alpha=0.8, fill_color="blue")
        glyph_g = VBar(x="x2", top="g_hist", bottom=0, width=0.5, fill_alpha=0.8, fill_color="green")
        glyph_r = VBar(x="x3", top="r_hist", bottom=0, width=0.5, fill_alpha=0.8, fill_color="red")
        plot.add_glyph(source, glyph_b)
        plot.add_glyph(source, glyph_g)
        plot.add_glyph(source, glyph_r)

        script, div = components(plot)   

        return script, div
   