from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
#from web_app import db, login_manager, app
from flask_login import UserMixin, LoginManager, current_user
from flask_admin.contrib.sqla import ModelView, AdminIndexView


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app) # for login and authentication
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)    
    
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class MyModelView(ModelView):
    # if this fucntion returns true then that user can see a this mdoel and if false then can not see model
    def is_accessible(self):
        return current_user.is_authenticated

    # this defiens process to be performed when unallowed user try to access this model from admin route
    def inaccessible_callback(self, username):
        return 'You cannot view this page. You are not admin user'

class MyAdminIndexView(AdminIndexView):
    # if this fucntion returns true then that user can see a this mdoel and if false then can not see model
    def is_accessible(self):
        return current_user.is_authenticated

    # this defiens process to be performed when unallowed user try to access this model from admin route
    def inaccessible_callback(self, username):
        return 'You cannot view page'

admin = Admin(app, index_view=MyAdminIndexView())
admin.add_view(MyModelView(User, db.session))

if __name__ == "__main__":
    app.run(debug=True)