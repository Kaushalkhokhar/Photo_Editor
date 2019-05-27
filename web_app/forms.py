from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.html5 import IntegerRangeField
from web_app.model import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Usrname already taken. Please try a diffferent username')
    
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Email already taken. Please try a diffferent email')        


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

class AdminForm(FlaskForm):
    color = IntegerRangeField('Color', default=50)
    brightness = IntegerRangeField('Brightness', default=50)
    hpf = SelectField('HPF', choices=[('one', 'Blur'), ('two', 'median blur')])
    hpf_range = IntegerRangeField('HPF', default=50)
    lpf = SelectField('LPF', choices=[('one', 'Blur'), ('two', 'median blur')])
    lpf_range = IntegerRangeField('LPF')
    submit = SubmitField('Submit', default=50)

class MethodForm(FlaskForm):
    method1 = BooleanField('Convolution', default=True)
    method2 = BooleanField('Averaging', default=True)
    method3 = BooleanField('Gaussian Blur', default=True)
    method4 = BooleanField('Median Blur', default=True)
    method5 = BooleanField('Bilateral Blur', default=True)
    method6 = BooleanField('Addition', default=True)
    method7 = BooleanField('Substraction', default=True)
    method8 = BooleanField('Multiplication', default=True)
    method9 = BooleanField('Not defined', default=True)

class GeneralForm(FlaskForm):
    color = IntegerRangeField('Color', default=50)
    brightness = IntegerRangeField('Brightness', default=50)
    other = IntegerRangeField('Other', default=50)

class FilterForm(FlaskForm):
    other = SelectField('Other', choices=[('one', 'one'), ('two', 'two'), ('three', 'three')])
    kernal = SelectField('Kernal', choices=[('one', '3 * 3'), ('two', '5 * 5')])