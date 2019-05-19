from flask import Flask, render_template, flash, redirect, url_for, request
from forms import ImageUpload

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisissecret'

@app.route('/')
@app.route('/home')
def home():
    return render_template('home1.html', title='Home')


@app.route('/upload', methods = ['GET', 'POST'])
def upload_image():    
        
        form = ImageUpload()   
        
        if form.validate_on_submit():
            flash('Image is submitted', 'success')
            return redirect(url_for('home'))       

        return render_template('upload_image.html', title='Home', form=form)

if __name__ == '__main__':
    app.run(debug=True)