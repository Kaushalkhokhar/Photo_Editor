from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.file import FileRequired, FileField, FileAllowed

class ImageUpload(FlaskForm):
    image = FileField('Image', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField('Upload')