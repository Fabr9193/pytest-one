from config import db
from models import User,Group

# Data to initialize database with
users = [
    {'name': 'Fabricio', 'token': 'faketoken4242'},
    {'name': 'Matthieu', 'token': 'faske42421'},
    {'name': 'Francois','token': 'faske443721'}
]


# Create the database
db.create_all()
db.session.commit()
# Iterate 
for item in users:
    u = User(token=item['token'], name=item['name'])
    db.session.add(u)

db.session.commit()