import os, cv2
import time
from PIL import Image
import shutil
import random
import numpy as np
from werkzeug.datastructures import MultiDict
from flask import render_template, flash, redirect, url_for, request, send_from_directory
from bokeh.embed import components
from web_app import app, APP_ROOT, bcrypt, db, mail, admin_user
from web_app.image_processing import Image_processing
from web_app.spectograph import Spectograph 
from bokeh.plotting import figure, show, output_file, save
from bokeh.models import ColumnDataSource
from bokeh.models.glyphs import VBar
from bokeh.embed import components
from web_app.forms import (RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm, \
                             AdminForm, MethodForm, GeneralForm, HistogramForm) 
from web_app.model import User, Methods
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

@app.route('/admin')
def admin():
    if not (current_user.is_authenticated and current_user.email == admin_user):
        flash('Please login as admin user', 'info')
        return redirect(url_for('login'))

    return "you are now in admin zone"

@app.route('/database')
def database():
    if not (current_user.is_authenticated and current_user.email == admin_user):
        flash('Please login as admin user', 'info')
        return redirect(url_for('login'))
    original = os.path.join(APP_ROOT, str(current_user.username) + '_original/')
    
    if not os.listdir(original):
        flash('Upload File', 'info')
        return redirect(url_for('upload'))

    original = os.path.join(APP_ROOT, str(current_user.username) + '_original/')
    filename = os.listdir(original)[0] 
    methods = Methods.query.all()
    return render_template('database.html', filename=filename, methods=methods, admin_user=admin_user)

@app.route('/')
@app.route('/home')
def home():           
    return render_template('home.html', title='Home', admin_user=admin_user)

@app.route('/upload')
def upload():
    
    
    if current_user.is_authenticated:
        if current_user.email == admin_user:
            original = os.path.join(APP_ROOT, str(current_user.username) + '_original/')
            original_two = os.path.join(APP_ROOT, str(current_user.username) + '_original_two/')
            second = os.path.join(APP_ROOT, str(current_user.username) + '_second/')
            result = os.path.join(APP_ROOT, str(current_user.username) + '_result/')
            result_specto = os.path.join(APP_ROOT, str(current_user.username) + '_result_specto/')
            
            if os.path.isdir(original):
                shutil.rmtree(original)
                shutil.rmtree(original_two)
                shutil.rmtree(second)
                shutil.rmtree(result)
                shutil.rmtree(result_specto)                
                os.mkdir(original)
                os.mkdir(second)
                os.mkdir(result)
                os.mkdir(original_two)
                os.mkdir(result_specto)
                
            else:    
                os.mkdir(original)
                os.mkdir(second)
                os.mkdir(result)
                os.mkdir(original_two)
                os.mkdir(result_specto)
                
        else:
            original = os.path.join(APP_ROOT, str(current_user.username) + '_original/')
            result = os.path.join(APP_ROOT, str(current_user.username) + '_result/')
            result_specto = os.path.join(APP_ROOT, str(current_user.username) + '_result_specto/')
            if os.path.isdir(original):
                shutil.rmtree(original)
                shutil.rmtree(result)
                shutil.rmtree(result_specto)
                os.mkdir(original)
                os.mkdir(result)
                os.mkdir(result_specto)
            else:    
                os.mkdir(original)
                os.mkdir(result)
                os.mkdir(result_specto)

        
    else:
        return redirect(url_for('login'))       
        
    return render_template('upload.html', title='Upload', admin_user=admin_user)

@app.route('/processing_display', methods = ['GET', 'POST'])
def processing_display():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))  
    
    original = os.path.join(APP_ROOT, str(current_user.username) + '_original/')

    if not os.listdir(original):    
        #To get the files uploaded to home page and stores it to target directory
        for file in request.files.getlist('image'):
            filename = file.filename     
            if not os.listdir(original):
                destination = "/".join([original, filename])                
                file.save(destination)       
    
    return render_template('processing_display.html')

@app.route('/display', methods = ['GET', 'POST'])
def display_image():  
    
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    methods = Methods.query.all() 
    
    original = os.path.join(APP_ROOT, str(current_user.username) + '_original/')

    #if not os.listdir(original):
    if os.listdir(original):    
        #To get the files uploaded to home page and stores it to target directory
        #for file in request.files.getlist('image'):
        #filename = file.filename
        filename = os.listdir(original)[0]
        '''if not os.listdir(original):
            destination = "/".join([original, filename])                
            file.save(destination)'''
        
        img = cv2.imread("/".join([original, filename]))
        height, width, cha = img.shape
        if height > 600:
            scale = 600/ height
            height = scale * height
            width = scale * width
            if width > 1000:
                scale = 1000 / width
                height = scale * height
                width = scale * width
        elif width > 1000:
            scale = 1000/width
            height = scale * height
            width = scale * width
            if height > 600:
                scale = 600 / width
                height = scale * height
                width = scale * width

        height = int(height)
        width = int(width)

        dim = (width, height)
        # resize image
        resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
                    
        shutil.rmtree(original)
        os.mkdir(original)
        destination = "/".join([original, filename])                                
        b, g, r = cv2.split(resized)
        resized = cv2.merge((r,g,b)) 
        im = Image.fromarray(resized)
        im.save(destination)   

    else:
        return redirect(url_for('upload'))
        #filename = os.listdir(original)[0]   
    
    
    '''image = cv2.imread(os.path.join(original, filename))
    height, width, cha = image.shape
    
    scale = 590 / height
    height = scale * height
    width = scale * width
    if width > 1380:
        scale = 1380 / width
        height = scale * height
        width = scale * width'''
      

    # return send_from_directory('static', filename, as_attachment=True) # Can be used to download the uploaded images
    return render_template('display.html', filename=filename, 
                            methods=methods, admin_user=admin_user) # In this filename will be the name of image file which is uploaded last in all files                

@app.route('/processing_processing/<filename>/<method>', methods = ['GET', 'POST'])
def processing_processing(filename, method):
    if not current_user.is_authenticated:
        return redirect(url_for('login')) 

    original = os.path.join(APP_ROOT, str(current_user.username) + '_original/')

    if not os.listdir(original):
        return redirect(url_for('upload'))         
    
    return render_template('processing_processing.html',filename=filename, method=method)

@app.route('/processing/<filename>/<method>', methods=['GET', 'POST'])
def processing(filename, method):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    elif Methods.query.filter_by(method_id=method).first().active_state == False:
        flash('This method is not allowed for you. Please try different one', 'info')
        return redirect(url_for('display_image'))

    original = os.path.join(APP_ROOT, str(current_user.username) + '_original/')

    if not os.listdir(original):
        return redirect(url_for('upload'))
    
    filename = os.listdir(original)[0]    
    
    image = cv2.imread(os.path.join(original, filename))
    height, width, cha = image.shape
    scale = 590/ height
    height = scale * height
    width = scale * width
    if width > 1380:
        scale = 1380 / width
        height = scale * height
        width = scale * width
        
    
    methods = Methods.query.all() 

    #processing the image based on reference link and method attached to that link
    if Methods.query.filter_by(method_id=method).first().image_operation ==  "Addition":             
        filename= Image_processing().addition(method, current_user)       
    elif Methods.query.filter_by(method_id=method).first().image_operation ==  "Subtraction":                  
        filename = Image_processing().subtraction(method, current_user)           
    elif Methods.query.filter_by(method_id=method).first().image_operation ==  "Multiplication":            
        filename = Image_processing().multiplication(method, current_user)    
        
    # we need to store processed file in our static folder then we can render by giving filename qual to our processed file 
    return render_template('processing.html', filename=filename, method=method, \
                            height=height, methods=methods, admin_user=admin_user)

@app.route('/processing_load_chart//<method>/<end_point>', methods = ['GET', 'POST'])
def processing_load_chart(method, end_point):
    return render_template('processing_load_chart.html',end_point=end_point, method=method)

@app.route('/load_chart/<method>/<end_point>', methods=['GET', 'POST'])
def load_chart(method, end_point):
                
    filename1 = str(random.randint(0,1000)*random.randint(1000,2000))
    filename2 = str(random.randint(2000,3000)*random.randint(3000,4000))
    
    # Here Method means method-id of current working method. and filename means name of file store in result folder.
    # if end_point == 'processing' or method == 'original':
    return_url = request.referrer # get the url from which request has initiated.
    spect = Spectograph()
    script, div = spect.spectograph_plot(current_user) 
    methods = Methods.query.all()

    return render_template('spectograph2.html', scripts=script, div=div, \
                            return_url=return_url, filename2=filename2, \
                            admin_user=admin_user, methods=methods)              
    
    '''else:
        return_url = request.referrer
        spect = Spectograph()
        script, div = spect.histogram_plot(current_user)
        form = HistogramForm()

        if request.method == 'POST' :
            method = Methods.query.filter_by(method_id=method).first()
            
            method.black_point = form.black_point.data
            method.midetone_slider = form.midetone_slider.data
            method.white_point = form.white_point.data
            db.session.commit()
            black_point = form.black_point.data
            midetone_slider = form.midetone_slider.data
            white_point = form.white_point.data
            Image_processing().LevelAdjustment(black_point, midetone_slider, white_point, current_user)
        
        return render_template('histogram.html', scripts=script, div=div, return_url=return_url,
                                form=form, filename1=filename1, filename2=filename2, \
                                admin_user=admin_user)'''

@app.route('/desplay_original/<filename>', methods=['GET', 'POST'])
def show_original_two(filename):
    original = os.path.join(APP_ROOT, str(current_user.username) + '_original/')
    original_two = os.path.join(APP_ROOT, str(current_user.username) + '_original_two/')
    filename = os.listdir(original_two)    
    if not filename:
        filename = os.listdir(original)[0]
        return send_from_directory(str(current_user.username) + '_original', filename)
    else:
        filename = filename[0]
        return send_from_directory(str(current_user.username) + '_original_two', filename)

@app.route('/display_second/<filename>', methods=['GET', 'POST'])
def show_second(filename):
    original = os.path.join(APP_ROOT, str(current_user.username) + '_original/')
    second = os.path.join(APP_ROOT, str(current_user.username) + '_second/')
    filename = os.listdir(second)    
    if not filename:
        filename = os.listdir(original)[0]
        return send_from_directory(str(current_user.username) + '_original', filename)
    else:
        filename = filename[0]
        return send_from_directory(str(current_user.username) + '_second', filename)
        
@app.route('/display_result/<filename>', methods=['GET', 'POST'])
def show_result(filename):
    original = os.path.join(APP_ROOT, str(current_user.username) + '_original/')
    result = os.path.join(APP_ROOT, str(current_user.username) + '_result/')
    if os.listdir(result):
        filename = os.listdir(result)[0]        
        return send_from_directory(str(current_user.username) + '_result', filename)        
    else:
        filename = os.listdir(original)[0]
        return send_from_directory(str(current_user.username) + '_original', filename)

@app.route('/display_result_specto/<filename>', methods=['GET', 'POST'])
def show_result_specto(filename):
    result_specto = os.path.join(APP_ROOT, str(current_user.username) + '_result_specto/')
    filename = os.listdir(result_specto)[0]
    return send_from_directory(str(current_user.username) + '_result_specto', filename)

@app.route('/download/<filename>', methods=['GET', 'POST'])
def download(filename):
    original = os.path.join(APP_ROOT, str(current_user.username) + '_original/')
    result = os.path.join(APP_ROOT, str(current_user.username) + '_result/')
    if os.listdir(result):
        filename = os.listdir(result)[0]        
        return send_from_directory(str(current_user.username) + '_result', filename=filename, as_attachment=True)        
    else:
        filename = os.listdir(original)[0]
        return send_from_directory(str(current_user.username) + '_original', filename=filename, as_attachment=True)

@app.route('/demo/', methods=['GET', 'POST'])
def demo():          
    return send_from_directory('sample_images', 'Untitled5.png')

@app.route('/demo_2/', methods=['GET', 'POST'])
def demo_2():          
    return send_from_directory('sample_images', 'input.png')

@app.route('/session', methods=['GET', 'POST'])
def new_session():
    if os.path.isdir(original_two):
        shutil.rmtree(original)
        shutil.rmtree(original_two)
        shutil.rmtree(second)
        shutil.rmtree(result)
        
        os.mkdir(original)
        os.mkdir(second)
        os.mkdir(result)
        os.mkdir(original_two)
        
    else:    
        os.mkdir(original)
        os.mkdir(second)
        os.mkdir(result)
        os.mkdir(original_two)
                   
    return redirect(url_for('upload'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:        
        return redirect(url_for('upload'))

    form = RegistrationForm()
    
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully. Now you can log in', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
        
    form = LoginForm()
    if form.validate_on_submit():
        
        user = User.query.filter_by(email=form.email.data).first()     
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('upload'))

        else:
            flash('login Unsuccessful. Please enter correct email and password', 'danger')
    
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    if current_user.email == admin_user:
        original = os.path.join(APP_ROOT, str(current_user.username) + '_original/')
        original_two = os.path.join(APP_ROOT, str(current_user.username) + '_original_two/')
        second = os.path.join(APP_ROOT, str(current_user.username) + '_second/')
        result = os.path.join(APP_ROOT, str(current_user.username) + '_result/')
        result_specto = os.path.join(APP_ROOT, str(current_user.username) + '_result_specto/')
        #To delete previous uploaded image and directory and creates new directory every time it runs home route    
        if os.path.isdir(original):
            shutil.rmtree(original)
            shutil.rmtree(original_two)
            shutil.rmtree(second)
            shutil.rmtree(result)
            shutil.rmtree(result_specto)
            
    else:
        original = os.path.join(APP_ROOT, str(current_user.username) + '_original/')
        result = os.path.join(APP_ROOT, str(current_user.username) + '_result/')
        result_specto = os.path.join(APP_ROOT, str(current_user.username) + '_result_specto/')
        if os.path.isdir(original):
            shutil.rmtree(original)
            shutil.rmtree(result)
            shutil.rmtree(result_specto)

    logout_user()
    return redirect(url_for('home'))

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='email@demo.com', #Can be other than email in init
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

@app.route('/processing_settings', methods = ['GET', 'POST'])
def processing_settings():
    method = "None"    
    if request.method == 'POST':
        form = AdminForm()
        if Methods.query.filter_by(method_id=form.method_id.data).first() is None:
            method = Methods(method_id=form.method_id.data, 
                            method_title=form.method_title.data, 
                            image_operation=dict(form.image_operation.choices).get(form.image_operation.data), 
                            result_contrast=form.result_contrast.data, 
                            result_brightness=form.result_brightness.data,
                            result_intensity=form.result_intensity.data, 
                            original_contrast=form.original_contrast.data, 
                            original_brightness=form.original_brightness.data, 
                            original_intensity=form.original_intensity.data, 
                            copy_contrast=form.copy_contrast.data, 
                            copy_brightness=form.copy_brightness.data, 
                            copy_intensity=form.copy_intensity.data, 
                            original_filter=dict(form.original_filter.choices).get(form.original_filter.data), 
                            original_kernal=dict(form.original_kernal.choices).get(form.original_kernal.data), 
                            copy_filter=dict(form.copy_filter.choices).get(form.copy_filter.data), 
                            copy_kernal=dict(form.copy_kernal.choices).get(form.copy_kernal.data),
                            original_black_point = form.original_black_point.data,
                            original_midetone_slider = form.original_midetone_slider.data,
                            original_white_point = form.original_white_point.data, 
                            copy_black_point = form.copy_black_point.data,
                            copy_midetone_slider = form.copy_midetone_slider.data,
                            copy_white_point = form.copy_white_point.data, 
                            result_black_point = form.result_black_point.data,
                            result_midetone_slider = form.result_midetone_slider.data,
                            result_white_point = form.result_white_point.data, 
                            active_state=form.active_state.data
                            )
            db.session.add(method)
            db.session.commit()

            method = form.method_id.data

        else:
            method = Methods.query.filter_by(method_id=form.method_id.data).first()
            method.image_operation = dict(form.image_operation.choices).get(form.image_operation.data)            
            method.method_title = form.method_title.data
            method.active_state = form.active_state.data
            method.original_contrast = form.original_contrast.data
            method.original_brightness = form.original_brightness.data
            method.original_intensity = form.original_intensity.data
            method.copy_contrast = form.copy_contrast.data
            method.copy_brightness = form.copy_brightness.data
            method.copy_intensity = form.copy_intensity.data
            method.result_contrast = form.result_contrast.data
            method.result_brightness = form.result_brightness.data
            method.result_intensity = form.result_intensity.data
            method.original_filter = dict(form.original_filter.choices).get(form.original_filter.data)
            method.original_kernal = dict(form.original_kernal.choices).get(form.original_kernal.data)
            method.copy_filter = dict(form.copy_filter.choices).get(form.copy_filter.data)
            method.copy_kernal = dict(form.copy_kernal.choices).get(form.copy_kernal.data)
            method.original_black_point = form.original_black_point.data
            method.original_midetone_slider = form.original_midetone_slider.data
            method.original_white_point = form.original_white_point.data
            method.copy_black_point = form.copy_black_point.data
            method.copy_midetone_slider = form.copy_midetone_slider.data
            method.copy_white_point = form.copy_white_point.data
            method.result_black_point = form.result_black_point.data
            method.result_midetone_slider = form.result_midetone_slider.data
            method.result_white_point = form.result_white_point.data
            db.session.commit()   

            method = form.method_id.data
    
    return render_template('processing_settings.html', method=method)

@app.route('/settings/<method>', methods=['GET', 'POST'])
def settings(method):
    if not (current_user.is_authenticated and current_user.email == admin_user):
        flash('Please login as admin user', 'info')
        return redirect(url_for('login'))
    original = os.path.join(APP_ROOT, str(current_user.username) + '_original/')
    
    if not os.listdir(original):
        flash('Upload file first', 'info')
        return redirect(url_for('upload')) 
    
    filename = os.listdir(original)[0]
    filename_original_two = os.listdir(original)[0]
    filename_second = os.listdir(original)[0]
    filename_result = os.listdir(original)[0]

    methods = Methods.query.all()
    file_name = [filename_original_two, filename_second, filename_result]

    if method != 'None':
        method_query = Methods.query.filter_by(method_id=method).first()
        form = AdminForm(formdata=MultiDict({'method_id': method_query.method_id,
                                             'image_operation': method_query.image_operation,
                                             'method_title': method_query.method_title,
                                             'active_state': method_query.active_state,
                                             'original_contrast': method_query.original_contrast,
                                             'original_brightness': method_query.original_brightness,
                                             'original_intensity': method_query.original_intensity,
                                             'copy_contrast': method_query.copy_contrast,
                                             'copy_brightness': method_query.copy_brightness,
                                             'copy_intensity': method_query.copy_intensity,
                                             'result_contrast': method_query.result_contrast,
                                             'result_brightness': method_query.result_brightness,
                                             'result_intensity': method_query.result_intensity,
                                             'original_filter': method_query.original_filter,
                                             'original_kernal': method_query.original_kernal,
                                             'copy_filter': method_query.copy_filter,
                                             'copy_kernal': method_query.copy_kernal,
                                             'original_black_point': method_query.original_black_point,
                                             'original_white_point': method_query.original_white_point,
                                             'original_midetone_slider': method_query.original_midetone_slider,
                                             'copy_black_point': method_query.copy_black_point,
                                             'copy_white_point': method_query.copy_white_point,
                                             'copy_midetone_slider': method_query.copy_midetone_slider,
                                             'result_black_point': method_query.result_black_point,
                                             'result_white_point': method_query.result_white_point,
                                             'result_midetone_slider': method_query.result_midetone_slider,
                                             }))

    else:
        form = AdminForm()
    
    #method = 1
    spect = Spectograph()
    script, div = spect.spectograph_plot(current_user)

    if method != "None":
        if method_query.image_operation ==  "Addition":             
            file_name = Image_processing().addition(method, current_user)       
        elif method_query.image_operation ==  "Subtraction":                  
            file_name = Image_processing().subtraction(method, current_user)           
        elif method_query.image_operation ==  "Multiplication":            
            file_name = Image_processing().multiplication(method, current_user)

        specto = Spectograph()
        script, div = specto.spectograph_plot(current_user)
        method = method

    '''if request_method == 'POST':
        
        if Methods.query.filter_by(method_id=form.method_id.data).first() is None:
            method = Methods(method_id=form.method_id.data, 
                            method_title=form.method_title.data, 
                            image_operation=dict(form.image_operation.choices).get(form.image_operation.data), 
                            result_contrast=form.result_contrast.data, 
                            result_brightness=form.result_brightness.data,
                            result_intensity=form.result_intensity.data, 
                            original_contrast=form.original_contrast.data, 
                            original_brightness=form.original_brightness.data, 
                            original_intensity=form.original_intensity.data, 
                            copy_contrast=form.copy_contrast.data, 
                            copy_brightness=form.copy_brightness.data, 
                            copy_intensity=form.copy_intensity.data, 
                            original_filter=dict(form.original_filter.choices).get(form.original_filter.data), 
                            original_kernal=dict(form.original_kernal.choices).get(form.original_kernal.data), 
                            copy_filter=dict(form.copy_filter.choices).get(form.copy_filter.data), 
                            copy_kernal=dict(form.copy_kernal.choices).get(form.copy_kernal.data),
                            original_black_point = form.original_black_point.data,
                            original_midetone_slider = form.original_midetone_slider.data,
                            original_white_point = form.original_white_point.data, 
                            copy_black_point = form.copy_black_point.data,
                            copy_midetone_slider = form.copy_midetone_slider.data,
                            copy_white_point = form.copy_white_point.data, 
                            result_black_point = form.result_black_point.data,
                            result_midetone_slider = form.result_midetone_slider.data,
                            result_white_point = form.result_white_point.data, 
                            active_state=form.active_state.data
                            )
            db.session.add(method)
            db.session.commit()

       else:
            method = Methods.query.filter_by(method_id=form.method_id.data).first()
            method.image_operation = dict(form.image_operation.choices).get(form.image_operation.data)            
            method.method_title = form.method_title.data
            method.active_state = form.active_state.data
            method.original_contrast = form.original_contrast.data
            method.original_brightness = form.original_brightness.data
            method.original_intensity = form.original_intensity.data
            method.copy_contrast = form.copy_contrast.data
            method.copy_brightness = form.copy_brightness.data
            method.copy_intensity = form.copy_intensity.data
            method.result_contrast = form.result_contrast.data
            method.result_brightness = form.result_brightness.data
            method.result_intensity = form.result_intensity.data
            method.original_filter = dict(form.original_filter.choices).get(form.original_filter.data)
            method.original_kernal = dict(form.original_kernal.choices).get(form.original_kernal.data)
            method.copy_filter = dict(form.copy_filter.choices).get(form.copy_filter.data)
            method.copy_kernal = dict(form.copy_kernal.choices).get(form.copy_kernal.data)
            method.original_black_point = form.original_black_point.data
            method.original_midetone_slider = form.original_midetone_slider.data
            method.original_white_point = form.original_white_point.data
            method.copy_black_point = form.copy_black_point.data
            method.copy_midetone_slider = form.copy_midetone_slider.data
            method.copy_white_point = form.copy_white_point.data
            method.result_black_point = form.result_black_point.data
            method.result_midetone_slider = form.result_midetone_slider.data
            method.result_white_point = form.result_white_point.data
            db.session.commit()

            if Methods.query.filter_by(method_id=form.method_id.data).first().image_operation ==  "Addition":             
                file_name = Image_processing().addition(form.method_id.data, current_user)       
            elif Methods.query.filter_by(method_id=form.method_id.data).first().image_operation ==  "Subtraction":                  
                file_name = Image_processing().subtraction(form.method_id.data, current_user)           
            elif Methods.query.filter_by(method_id=form.method_id.data).first().image_operation ==  "Multiplication":            
                file_name = Image_processing().multiplication(form.method_id.data, current_user)
            
            specto = Spectograph()
            script, div = specto.spectograph_plot(current_user)
            method = form.method_id.data'''


    return render_template('settings.html', form=form, filename=filename,
                            file_name=file_name,
                            scripts=script, div=div,
                            method=method, methods=methods,
                            admin_user=admin_user)

@app.route("/learning", methods=['GET', 'POST'])
def learning():    
    return render_template('learning.html')
