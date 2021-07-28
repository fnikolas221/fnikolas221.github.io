from flask_login import UserMixin
from . import db
import datetime
from pytz import timezone

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120),index=True,nullable=False)
    username = db.Column(db.String(64),index=True, unique=True,nullable=False)
    email = db.Column(db.String(120), index=True, unique= True,nullable=False)
    password = db.Column(db.LargeBinary(128))
    first_created_utc = db.Column(db.DateTime,nullable=False,default=datetime.now(tz=timezone('UTC')))
    
    #ONE TO MANY
    history = db.relationship('AdminHistory',backref='owner')
    userconfig = db.relationship('UserConfig',backref='owner')


    def __repr___(self):
        return '<User {}>'.format(self.username)
    
class AdminHistory(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    login_recorded_utc = db.Column(db.DateTime,nullable=False,default=datetime.now(tz=timezone('UTC')))

    # ONE TO MANY RELATIONSHIP
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))


class AppSetting(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    setting = db.Column(db.String(100),unique=True,nullable=False)
    configdesc = db.Column(db.String(500),nullable=False)
    hasconstrained = db.Column(db.Boolean,nullable=False)
    datatype = db.Column(db.String(100),nullable=False)
    minvalueOrDefault = db.Column(db.String(250))    
    maxvalue = db.Column(db.String(250))  
    userconfig = db.relationship('UserConfig',backref='has_a') 

class UserConfig(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    appsettingID = db.Column(db.Integer, db.ForeignKey('app_setting.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    configvalue = db.Column(db.String(250),nullable=False)