
from app import app
from models import db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import User, Book, Exchange

#Implementing Admin Dashboard:
#Create an admin dashboard to monitor platform activities, manage users, and moderate book listings and reviews.

admin = Admin(app)

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Book, db.session))
admin.add_view(ModelView(Exchange, db.session))
