from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.fields.html5 import IntegerRangeField
#from flask_wtf.html5 import IntegerRangeField
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

class AdminForm(FlaskForm):
    method_id = SelectField('Method ID', choices=[(str(i), str(i)) for i in range(1,11)])
    image_operations = SelectField('Operations', choices=[('one', 'Addition'), \
                                    ('two', 'Substraction'), ('three', 'Multiplication')])
    method_title = StringField('Title', validators=[DataRequired(), Length(min=2, max=20)])
    active_state = BooleanField('Active State',default=True)
    original_color = IntegerRangeField('Color', default=50)
    original_brightness = IntegerRangeField('Brightness', default=50)
    original_intensity = IntegerRangeField('Intensity', default=50)
    copy_color = IntegerRangeField('Color', default=50)
    copy_brightness = IntegerRangeField('Brightness', default=50)
    copy_intensity = IntegerRangeField('Intensity', default=50)
    result_color = IntegerRangeField('Color', default=50)
    result_brightness = IntegerRangeField('Brightness', default=50)
    result_intensity = IntegerRangeField('Intensity', default=50)
    original_filter = SelectField('Filter', choices=[('one', 'LPF'), ('two', 'HPF'), ('three', 'BPF')])
    original_kernal = SelectField('Kernal', choices=[('one', '3 * 3'), ('two', '5 * 5')])
    copy_filter = SelectField('Filter', choices=[('one', 'LPF'), ('two', 'HPF'), ('three', 'BPF')])
    copy_kernal = SelectField('Kernal', choices=[('one', '3 * 3'), ('two', '5 * 5')])    
    submit = SubmitField('Submit')
    
    
    # Privious Admin Panel Settings
    '''method1 = BooleanField('Convolution', default=True)
    method2 = BooleanField('Averaging', default=True)
    method3 = BooleanField('Gaussian Blur', default=True)
    method4 = BooleanField('Median Blur', default=True)
    method5 = BooleanField('Bilateral Blur', default=True)
    method6 = BooleanField('Addition', default=True)
    method7 = BooleanField('Substraction', default=True)
    method8 = BooleanField('Multiplication', default=True)
    method9 = BooleanField('Not defined', default=True)
    color = IntegerRangeField('Color', default=50)
    brightness = IntegerRangeField('Brightness', default=50)
    intensity = IntegerRangeField('Intensity', default=50)
    other = IntegerRangeField('Other', default=50)
    other = SelectField('Other', choices=[('one', 'one'), ('two', 'two'), ('three', 'three')])
    kernal = SelectField('Kernal', choices=[('one', '3 * 3'), ('two', '5 * 5')])
    submit = SubmitField('Submit')'''