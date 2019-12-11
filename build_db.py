from config import db
from models import User

# Data to initialize database with
users = [
    {'name': 'Fabricio', 'token': 'faketoken4242'},
    {'name': 'Matthieu', 'token': 'faske42421'},
    {'name': 'Francois','token': 'faske443721'}
]

# Create the database
db.create_all()

# Iterate 
# for User in users:
#     print(User['name'])
#     u = User(token=User['token'], name=User['name'])
#     db.session.add(u)

db.session.commit()