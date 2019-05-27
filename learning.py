from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerRangeField, PasswordField, TextAreaField, TextField, RadioField, SelectField, FileField, IntegerField, DateField
from wtforms.validators import InputRequired
import os
import os

app = Flask(__name__)
app.debug=True

app.config['SECRET_KEY'] = 'Thisisasecret!'

@app.route("/test", methods=["POST"])
def test():
    name_of_slider = request.form["name_of_slider"]
    return name_of_slider



if __name__=="__main__":
    app.run() 