from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import db,ma

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://atpwoaz1wdt9g74m:ab87fdzdl271b45v@q2gen47hi68k1yrb.chr7pe7iynqr.eu-west-1.rds.amazonaws.com:3306/rxu08ov7dxk37auw"
db = SQLAlchemy(app)

user_group = db.Table('user_group',
db.Column('user_id', db.Integer, db.ForeignKey('user.user_id')),
db.Column('group_id', db.Integer, db.ForeignKey('user.user_id')),
)

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(20))
    token = db.Column(db.String(64))
    groups = db.relationship('Group', secondary=user_group, backref=db.backref('user_groups'))
    def create_token(self):
        return secrets.token_urlsafe()

class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
        sqla_session = db.session
        
class Group(db.Model):
    __tablename__ = 'groups'
    group_id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(20))