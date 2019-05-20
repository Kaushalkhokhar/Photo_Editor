import os
from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
target = os.path.join(APP_ROOT, 'Images/') #To create path for storing image in local directory

processed_target = os.path.join(APP_ROOT, 'processed_images/') #To store processed image


from web_app import routes