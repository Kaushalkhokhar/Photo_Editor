from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
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
    method7 = BooleanField('Subtraction', default=True)
    method8 = BooleanField('Multiplication', default=True)
    method9 = BooleanField('Not defined', default=True)

class GeneralForm(FlaskForm):
    color = IntegerRangeField('Color', default=50)
    brightness = IntegerRangeField('Brightness', default=50)
    other = IntegerRangeField('Other', default=50)

class AdminForm(FlaskForm):
    method_id = SelectField('Method ID', choices=[(str(i), str(i)) for i in range(1,20)])
    image_operation = SelectField('Operations', choices=[('one', 'Addition'), \
                                    ('two', 'Subtraction'), ('three', 'Multiplication')])
    method_title = StringField('Title', validators=[DataRequired(), Length(min=2, max=20)])
    active_state = BooleanField('Active State',default=True)
    original_contrast = IntegerRangeField('Contrast', default=50)
    original_brightness = IntegerRangeField('Brightness', default=50)
    original_intensity = IntegerRangeField('Intensity', default=50)
    copy_contrast = IntegerRangeField('Contrast', default=50)
    copy_brightness = IntegerRangeField('Brightness', default=50)
    copy_intensity = IntegerRangeField('Intensity', default=50)
    result_contrast = IntegerRangeField('Contrast', default=50)
    result_brightness = IntegerRangeField('Brightness', default=50)
    result_intensity = IntegerRangeField('Intensity', default=50)
    original_filter = SelectField('Filter', choices=[('one', 'Without_Filter'), ('two', 'Averaging'), 
                                                    ('three', 'Gaussian_Blur'), ('four', 'Median_Blur'), 
                                                    ('five', 'Bilateral_Blur'), ('six', 'HPF'),
                                                    ('seven', 'LPF'), ('eight', 'BPF'),
                                                    ('nine', 'NOTCH')])
    copy_filter = SelectField('Filter', choices=[('one', 'Without_Filter'), ('two', 'Averaging'), 
                                                 ('three', 'Gaussian_Blur'), ('four', 'Median_Blur'), 
                                                 ('five', 'Bilateral_blur'), ('six', 'HPF'),
                                                 ('seven', 'LPF'), ('eight', 'BPF'),
                                                 ('nine', 'NOTCH')])

    original_kernal = SelectField('Kernal', choices=[('one', '3*3_First'), ('two', '3*3_Second'), 
                                                     ('three', '5*5_First'), ('four', '5*5_Second'),
                                                     ('five', '7*7_First'), ('six', '7*7_Second'),
                                                     ('seven', '9*9_First'), ('eight', '9*9_Second'),
                                                     ('nine', '11*11_First'), ('ten', '11*11_Second')])    
    copy_kernal = SelectField('Kernal', choices=[('one', '3*3_First'), ('two', '3*3_Second'), 
                                                 ('three', '5*5_First'), ('four', '5*5_Second'),
                                                 ('five', '7*7_First'), ('six', '7*7_Second'),
                                                 ('seven', '9*9_First'), ('eight', '9*9_Second'),
                                                 ('nine', '11*11_First'), ('ten', '11*11_Second')])
    original_black_point = IntegerField('Black Point', default=0, validators=[DataRequired(), NumberRange(min=0, max=127)])
    original_white_point = IntegerField('White Point', default=255, validators=[DataRequired(), NumberRange(min=128, max=255)])
    original_midetone_slider = FloatField('Middle Point', default=1, validators=[DataRequired(), NumberRange(min=0, max=2)])
    copy_black_point = IntegerField('Black Point', default=0, validators=[DataRequired(), NumberRange(min=0, max=127)])
    copy_white_point = IntegerField('White Point', default=255, validators=[DataRequired(), NumberRange(min=128, max=255)])
    copy_midetone_slider = FloatField('Middle Point', default=1, validators=[DataRequired(), NumberRange(min=0, max=2)])
    result_black_point = IntegerField('Black Point', default=0, validators=[DataRequired(), NumberRange(min=0, max=127)])
    result_white_point = IntegerField('White Point', default=255, validators=[DataRequired(), NumberRange(min=128, max=255)])
    result_midetone_slider = FloatField('Middle Point', default=1, validators=[DataRequired(), NumberRange(min=0, max=2)])
    submit = SubmitField('Submit')

class HistogramForm(FlaskForm):
    black_point = IntegerField('Black Point', validators=[DataRequired(), NumberRange(min=0, max=127)])
    white_point = IntegerField('White Point', validators=[DataRequired(), NumberRange(min=128, max=255)])
    midetone_slider = FloatField('Midetone Slider', validators=[DataRequired(), NumberRange(min=0, max=2)])
    submit = SubmitField('Submit')
    
    
   