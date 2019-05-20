import os
import shutil
from PIL import Image
from flask import Flask, render_template, flash, redirect, url_for, request, send_from_directory
from image_processing import convolution, averaging, median_blur, gaussian_blur, bilateral_blur

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisissecret'

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')


@app.route('/upload', methods = ['GET', 'POST'])
def upload_image():  

    method1 = "convolution"
    method2 = "averaging"
    method3 = "gaussian_blur"
    method4 = "median_blur"
    method5 = "bilateral_blur"

    if not request.files.getlist('image'):
        return redirect(url_for('home'))

    else:    
        target = os.path.join(APP_ROOT, 'Images/')
        print(target)

        if not os.path.isdir(target):
            os.mkdir(target)
        
        #for uploading multiple files at a time
        for file in request.files.getlist('image'):
            print(file)
            filename = file.filename
            destination = "/".join([target, filename])
            print(destination)
            file.save(destination)        
        
        # return send_from_directory('static', filename, as_attachment=True) # Can be used to download the uploaded images
        return render_template('upload.html', image_name=filename, method1=method1, method2=method2, \
                                method3=method3, method4=method4, method5=method5) # In this filename will be the name of image file which is uploaded last in all files

@app.route('/upload/<filename>', methods=['GET', 'POST'])
def show(filename):
    print(filename)   
    return send_from_directory('images', filename)

@app.route('/processing/<filename>/<method>', methods=['GET', 'POST'])
def processing(filename, method):

    method1 = "convolution"
    method2 = "averaging"
    method3 = "gaussian_blur"
    method4 = "median_blur"
    method5 = "bilateral_blur"

    if method ==  "convolution":       
        filename = convolution(plotting=False)
    elif method ==  "averaging":   
        filename = averaging(plotting=False)    
    elif method ==  "gaussian_blur":      
        filename = gaussian_blur(plotting=False)
    elif method ==  "median_blur":    
        filename = median_blur(plotting=False)    
    elif method ==  "bilateral_blur":    
        filename = bilateral_blur(plotting=False)
    
    # we need to store processed file in our static folder then we can render by giving filename qual to our processed file 
    return render_template('processing.html', image_name=filename, method1=method1, method2=method2, \
                                method3=method3, method4=method4, method5=method5)

@app.route('/processed/<filename>', methods=['GET', 'POST'])
def processed_image(filename):           
    return send_from_directory('processed_images', filename)

@app.route('/bootstrap', methods=['GET', 'POST'])
def bootstrap():        
    return render_template('chart.html')

if __name__ == '__main__':
    app.run(debug=True)