import os, cv2
import shutil
import random
import numpy as np
from flask import render_template, flash, redirect, url_for, request, send_from_directory
from bokeh.embed import components
from web_app import app, original, APP_ROOT, processed_target, second_img, bcrypt, db, mail
from web_app.image_processing import image_operations
from web_app.histogram import Histogram 
from bokeh.plotting import figure, show, output_file, save
from bokeh.models import ColumnDataSource
from bokeh.models.glyphs import VBar
from bokeh.embed import components
from web_app.forms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm
from web_app.model import User
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

"""APP_ROOT = os.path.dirname(os.path.abspath(__file__))
target = os.path.join(APP_ROOT, 'Images/') #To create path for storing image in local directory"""


@app.route('/')
@app.route('/home')
def home():     
    return render_template('home.html', title='Home')

@app.route('/upload')
def upload():
    #To delete previous uploaded image and directory and creates new directory every time it runs home route    
    if os.path.isdir(original):
        shutil.rmtree(original)
        shutil.rmtree(second_img)
        shutil.rmtree(processed_target)
        os.mkdir(original)
        os.mkdir(second_img)
        os.mkdir(processed_target)
    else:    
        os.mkdir(original)
        os.mkdir(second_img)
        os.mkdir(processed_target)
    
    return render_template('upload.html', title='Upload')

@app.route('/display', methods = ['GET', 'POST'])
def display_image():  
    #To render this method to link for decision making
    method1 = "convolution"
    method2 = "averaging"
    method3 = "gaussian_blur"
    method4 = "median_blur"
    method5 = "bilateral_blur"

    #if image is not uploaded in file field of home template then return to home again else executes the code given
    if not request.files.getlist('image'):
        return redirect(url_for('upload'))

    else:
        if not os.path.isdir(original):#Creates direcotry if not, else passes it
            os.mkdir(original) 
        
        #To get the files uploaded to home page and stores it to target directory
        for file in request.files.getlist('image'):
            print(file)
            filename = file.filename
            destination = "/".join([original, filename])
            print(destination)
            file.save(destination)        
        
        # return send_from_directory('static', filename, as_attachment=True) # Can be used to download the uploaded images
        return render_template('display.html', filename=filename, method1=method1, method2=method2, \
                                method3=method3, method4=method4, method5=method5) # In this filename will be the name of image file which is uploaded last in all files

@app.route('/display/<filename>', methods=['GET', 'POST'])
def show(filename):
    print(filename)   
    return send_from_directory('Original', filename)

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
    hist = Histogram()
    script, div, method = hist.histogram_plot()        
    return render_template('histogram.html', scripts=script, div=div, filename=filename, method=method)



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
    if current_user.is_authenticated:
        return redirect(url_for('upload'))
        
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