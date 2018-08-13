from flask import Flask

app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy

import os

if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else: 
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)

from flask_bootstrap import Bootstrap
Bootstrap(app)

# import models
from application.people import models
from application.auth import models
from application.articles import models
from application.issues import models


# authentication
from application.auth.models import User
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Login required"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

try:
    db.create_all()
except Exception as err:
    print(err)
    pass

from application.issues.models import Issue
@app.context_processor
def set_global_current():
    try:
        current = Issue.query.filter_by(current=True).first().name
    except:
        current = ""
    return dict(current=current)

# import views
from application import views
from application.people import views
from application.auth import views
from application.articles import views
from application.issues import views
