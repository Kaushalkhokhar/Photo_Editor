import os, cv2
import shutil
import random
import numpy as np
from flask import render_template, flash, redirect, url_for, request, send_from_directory
from bokeh.embed import components
from web_app import app, target, APP_ROOT, processed_target
from web_app.image_processing import image_operations
from bokeh.plotting import figure, show, output_file, save
from bokeh.models import ColumnDataSource
from bokeh.models.glyphs import VBar
from bokeh.embed import components
from web_app.histogram import histogram_plot


"""APP_ROOT = os.path.dirname(os.path.abspath(__file__))
target = os.path.join(APP_ROOT, 'Images/') #To create path for storing image in local directory"""

@app.route('/')
@app.route('/home')
def home():
    #To delete previous uploaded image and directory and creates new directory every time it runs home route    
    if os.path.isdir(target):
        shutil.rmtree(target)            
        os.mkdir(target)
    else:    
        os.mkdir(target)

    return render_template('home.html', title='Home')

@app.route('/upload', methods = ['GET', 'POST'])
def upload_image():  
    #To render this method to link for decision making
    method1 = "convolution"
    method2 = "averaging"
    method3 = "gaussian_blur"
    method4 = "median_blur"
    method5 = "bilateral_blur"

    #if image is not uploaded in file field of home template then return to home again else executes the code given
    if not request.files.getlist('image'):
        return redirect(url_for('home'))

    else:
        if not os.path.isdir(target):#Creates direcotry if not, else passes it
            os.mkdir(target) 
        
        #To get the files uploaded to home page and stores it to target directory
        for file in request.files.getlist('image'):
            print(file)
            filename = file.filename
            destination = "/".join([target, filename])
            print(destination)
            file.save(destination)        
        
        # return send_from_directory('static', filename, as_attachment=True) # Can be used to download the uploaded images
        return render_template('upload.html', filename=filename, method1=method1, method2=method2, \
                                method3=method3, method4=method4, method5=method5) # In this filename will be the name of image file which is uploaded last in all files

@app.route('/upload/<filename>', methods=['GET', 'POST'])
def show(filename):
    print(filename)   
    return send_from_directory('images', filename)

@app.route('/processing/<filename>/<method>', methods=['GET', 'POST'])
def processing(filename, method):
    #To delete previous processes image and cirectory and creates new directory every time it runs processing
    #target = os.path.join(APP_ROOT, 'processed_images/') #To store processed image
    if os.path.isdir(processed_target):
        shutil.rmtree(processed_target)            
        os.mkdir(processed_target)
    else:    
        os.mkdir(processed_target)

    #To render this method to link for decision making
    method1 = "convolution"
    method2 = "averaging"
    method3 = "gaussian_blur"
    method4 = "median_blur"
    method5 = "bilateral_blur"     

    #processing the image based on reference link and method attached to that link
    if method ==  "convolution":
        convo = image_operations()      
        filename = convo.convolution(plotting=False)       
    elif method ==  "averaging":        
        avrg = image_operations()   
        filename = avrg.averaging(plotting=False)           
    elif method ==  "gaussian_blur":
        gblur = image_operations()      
        filename = gblur.gaussian_blur(plotting=False)
    elif method ==  "median_blur":    
        mblur = image_operations()
        filename = mblur.median_blur(plotting=False)
    elif method ==  "bilateral_blur":    
        bblur = image_operations()
        filename = bblur.bilateral_blur(plotting=False)
    
    # we need to store processed file in our static folder then we can render by giving filename qual to our processed file 
    return render_template('processing.html', filename=filename, method1=method1, method2=method2, \
                                method3=method3, method4=method4, method5=method5)

@app.route('/processed/<filename>', methods=['GET', 'POST'])
def processed_image(filename):                   
    return send_from_directory('processed_images', filename=filename)

@app.route('/load_chart/<filename>', methods=['GET', 'POST'])
def load_chart(filename):

    script, div, method = histogram_plot()        
    return render_template('histogram.html', scripts=script, div=div, filename=filename, method=method)




@app.route('/testing', methods=['GET', 'POST'])
def testing():
    """
    if bars_count <= 0:
        bars_count = 1   

    data = {"days": [], "bugs": [], "bugs_2": [],"costs": []}
    for i in range(1, bars_count + 1):
        data['days'].append(i)
        data['bugs'].append(random.randint(1,100))
        data['bugs_2'].append(random.randint(1,100))
        data['costs'].append(random.uniform(1.00, 1000.00))

    chart_class = chart_layout()   

    hover = chart_class.create_hover_tool()
    plot = chart_class.create_bar_chart(data, "Bugs found per day", "days", 
                            "bugs", "bugs_2", hover)
    script, div = components(plot)

    return render_template("chart.html", bars_count=bars_count,
                           the_div=div, the_script=script)"""