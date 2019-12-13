from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import db,ma
import secrets

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://atpwoaz1wdt9g74m:ab87fdzdl271b45v@q2gen47hi68k1yrb.chr7pe7iynqr.eu-west-1.rds.amazonaws.com:3306/rxu08ov7dxk37auw"

user_group = db.Table('user_group',
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('group.group_id'), primary_key=True)
)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(20))
    token = db.Column(db.String(64))
    tags = db.relationship('Group', secondary=user_group, lazy='subquery',
        backref=db.backref('groups', lazy=True))
    def create_token():
        return secrets.token_urlsafe()

class Group(db.Model):
    group_id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(20))