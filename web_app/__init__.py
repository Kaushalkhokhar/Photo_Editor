import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app) # for database
bcrypt = Bcrypt(app) # for hashing the passsword to store
login_manager = LoginManager(app) # for login and authentication
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'admin@demo.com' #Any email id from that we want to send message
app.config['MAIL_PASSWORD'] = 'pasword' #Login password for that email account
mail = Mail(app)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
original = os.path.join(APP_ROOT, 'Original/') #To create path for storing image in local directory
processed_target = os.path.join(APP_ROOT, 'processed_images/') #To store processed image
second_img = os.path.join(APP_ROOT, 'Second/')

from web_app import routes