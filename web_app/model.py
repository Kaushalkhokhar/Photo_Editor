from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from web_app import db, login_manager, app, admin_user
from flask_login import UserMixin, current_user
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.LargeBinary)
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

class Methods(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    method_id = db.Column(db.Integer, nullable=False)
    method_title = db.Column(db.String(50), nullable=False)
    image_operation = db.Column(db.String, default="Addition")
    result_contrast = db.Column(db.Integer, default=50)

    result_brightness = db.Column(db.Integer, default=50)
    result_intensity = db.Column(db.Integer, default=50)
    original_contrast = db.Column(db.Integer, default=50)
    original_brightness = db.Column(db.Integer, default=50)
    original_intensity = db.Column(db.Integer, default=50)
    copy_contrast = db.Column(db.Integer, default=50)
    copy_brightness = db.Column(db.Integer, default=50)
    copy_intensity = db.Column(db.Integer, default=50)
    original_filter = db.Column(db.String, default="averaging")
    original_kernal = db.Column(db.String, default="3*3")
    copy_filter = db.Column(db.String, default="averaging")
    copy_kernal = db.Column(db.String, default="3*3")
    black_point = db.Column(db.Integer,default=0)
    midetone_slider = db.Column(db.Float, default=1)
    white_point = db.Column(db.Integer, default=255)
    active_state = db.Column(db.Boolean, default=True)
    #active_state = db.Column(db.Boolean, default=True)    
    #kernal = db.Column(db.String(20), default="3*3")
    #other = db.Column(db.String(20), default="other")

    def __repr__(self):
        return f"Methods('{self.method_title}', '{self.method_id}')"
    

class MyModelView(ModelView):
    # if this fucntion returns true then that user can see a this mdoel and if false then can not see model
    def is_accessible(self):
        return current_user.email == admin_user

    # this defiens process to be performed when unallowed user try to access this model from admin route
    def inaccessible_callback(self, username):
        return 'You cannot view this page. You are not admin user'

class MyAdminIndexView(AdminIndexView):
    # if this fucntion returns true then that user can see a this mdoel and if false then can not see model
    def is_accessible(self):
        return current_user.email == admin_user
    # this defiens process to be performed when unallowed user try to access this model from admin route
    def inaccessible_callback(self, username):
        return 'You cannot view page'

admin = Admin(app, index_view=MyAdminIndexView())
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Methods, db.session))




