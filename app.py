from flask import Flask,request,jsonify
from config import db
from models import User, UserSchema, Group, GroupSchema
import json
import requests

# Init
app  = Flask(__name__)
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://atpwoaz1wdt9g74m:ab87fdzdl271b45v@q2gen47hi68k1yrb.chr7pe7iynqr.eu-west-1.rds.amazonaws.com:3306/rxu08ov7dxk37auw'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Methods

def authenticate(username):
    print(username)
    user = User()
    user.name = username
    user.token = User.create_token()
   
    # Add the user to the database
    db.session.add(user)
    db.session.commit()
    return "Success ! Token is : " + user.token , 201

def user_associate(given_token, element_type):
    user = User.query.filter_by(token=given_token).first()
    #TODO check if he doesnt already have group
    if (check_element_type(element_type)):
        group = Group.query.filter_by(name=element_type).first()
        if group is None:
            group = Group()
            group.name = element_type
            db.session.add(group)
        user.groups.append(group)
    else:
        return "Type does not exist", 400
    db.session.commit()
    return "Added to " + user.name + " the type " + group.name, 200

def user_remove(given_token, element_type):
    user = User.query.filter_by(token=given_token).first()
    #TODO check if he doesnt already have group
    if (check_element_type(element_type)):
        group = Group.query.filter_by(name=element_type).first()
        if group is None:
            group = Group()
            group.name = element_type
            db.session.add(group)
        user.groups.remove(group)
    else:
        return "Type does not exist", 400
    db.session.commit()
    return "Removed to " + user.name + " the type " + group.name, 200


def check_element_type(element_type):
    all_types = get_element_types()
    return element_type in all_types

def get_element_types():
    link = 'https://pokeapi.co/api/v2/type'
    data = []
    res = requests.get(link)
    jsondata = json.loads(res.text)
    for i in jsondata['results']:
      data.append(i['name'])
    return(data)

def user_show(given_token):
    user = User.query.filter_by(token=given_token).first()
    print(type(user))
    if user is not None:
        user_schema = UserSchema()
        res = user_schema.dump(user)
        print(res)
        return jsonify({'user' : res}), 200
    else:
        return "Not Found", 404


# Routes
@app.route('/')
def hello():
    return "Hello World!"

@app.route('/api/login', methods=['POST'])
def login():
    user = request.args['user']
    return authenticate(user)

@app.route('/api/group/<element_type>/add', methods=['POST'])
def associate(element_type=None):
    token = request.args['token']
    return user_associate(element_type=element_type,given_token=token)

@app.route('/api/group/<element_type>/remove', methods=['POST'])
def remove(element_type=None):
    token = request.args['token']
    return user_remove(element_type=element_type,given_token=token)

@app.route('/api/user/me', methods=['GET'])
def show():
    token = request.args['token']
    return user_show(given_token=token)
    
if __name__ == '__main__':
    db.init_app(app)
    app.run()