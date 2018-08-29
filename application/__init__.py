from flask import Flask

app = Flask(__name__)

# tools to hash passwords
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
app.config["BCRYPT_HANDLE_LONG_PASSWORDS"] = True

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
from application.pictures import models


# authentication
from application.auth.models import User
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager, current_user
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Login required"

from functools import wraps
from application.auth.models import Role

# thank you for the example, anonOstrich/peliloki
def login_required(role="ANY"):    
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            
            unauthorized = False

            if role != "ANY":
                unauthorized = False
            
            unauthorized = current_user.has_role(role)
            
            if unauthorized: 
                return login_manager.unauthorized()
            
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

try:
    db.create_all()
    admin_role = Role("ADMIN")
    editor_role = Role("EDITOR")
    language_consultant_role = Role("LANGUAGE_CONSULTANT")
    picture_editor_role = Role("PICTURE_EDITOR")
    layout_artist_role = Role("LAYOUT_ARTIST")
    db.session.add_all((admin_role, language_consultant_role, picture_editor_role, layout_artist_role))
    db.session.commit()
    if os.environ.get("ADMIN_PW"):
        print("ADMIN_PW:", os.environ.get("ADMIN_PW"))
        admin = User(username="admin", name="Admin Admin", plaintext_password=os.environ.get("ADMIN_PW"))
        db.session.add(admin)
        db.session.commit()
        admin.add_roles(admin_role, editor_role, language_consultant_role, picture_editor_role, layout_artist_role)
        db.session.add(admin)
    db.session.commit()
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

@app.context_processor
def set_global_issues():
    issuenames = []
    try:
        issues = Issue.query.all()
        for issue in issues:
            issuenames.append(issue.name)
    except:
        pass
    return dict(issuenames=issuenames)
        

# import views
from application import views
from application.people import views
from application.auth import views
from application.articles import views
from application.issues import views
from application.pictures import views
