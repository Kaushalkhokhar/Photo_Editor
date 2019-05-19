import os
from PIL import Image
from flask import Flask, render_template, flash, redirect, url_for, request, send_from_directory
from image_processing import convolution

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisissecret'

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')


@app.route('/upload', methods = ['GET', 'POST'])
def upload_image():  

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

        process = "True"
        
        # return send_from_directory('static', filename, as_attachment=True) # Can be used to download the uploaded images
        return render_template('upload.html', image_name=filename) # In this filename will be the name of image file which is uploaded last in all files

@app.route('/upload/<filename>', methods=['GET', 'POST'])
def show(filename):
    print(filename)   
    return send_from_directory('images', filename)

@app.route('/processing/<filename>', methods=['GET', 'POST'])
def processing(filename):

    print(filename)

    target = os.path.join(APP_ROOT, 'processed_images/')
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    processed_image = convolution(filename, plotting=False)
    destination = "/".join([target, filename])
    print(destination)
    im = Image.fromarray(processed_image)
    im.save(destination)
    
    # we need to store processed file in our static folder then we can render by giving filename qual to our processed file 
    return render_template('processing.html', image_name=filename)

@app.route('/processed/<filename>', methods=['GET', 'POST'])
def processed_image(filename):
    print(filename)        
    return send_from_directory('processed_images', filename)



@app.route('/bootstrap', methods=['GET', 'POST'])
def bootstrap():        
    return render_template('bootstrap.html')



if __name__ == '__main__':
    app.run(debug=True)