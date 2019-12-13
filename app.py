from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import User,Group
import json
import requests

# Init
app  = Flask(__name__)

# Methods

def authenticate(username):
    user = User(username, token=User.create_token())
    existing_user = (
    User.query.filter(User.token == token)
    .one_or_none())
    if existing_user is None:

        schema = UserSchema()
        new_user = schema.load(user, session=db.session).data

        # Add the user to the database
        db.session.add(new_user)
        db.session.commit()

        # Serialize and return the newly created user in the response
        data = schema.dump(new_user).data

        return data, 201
    else :
        abort(
            409,
            "User with token {token} exists already".format(
                token
            ),
        )

def check_element_type(element_type):
    link = 'https://pokeapi.co/api/v2/type'
    res = requests.get(link)
    print(res.text)
    return False

# def user_associate(element_type):


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
    return user_associate(element_type, token)

@app.route('/api/group/<element_type>/remove', methods=['POST'])
def remove(elment_type=None):
    token = request.args['token']
    return User.remove(element_type, token)

@app.route('/api/user/me')
def show():
    token = request.args['token']
    return User.show(token)
    
if __name__ == '__main__':
    app.run()