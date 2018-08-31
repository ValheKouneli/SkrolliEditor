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
from application.auth.models import Role, UserRole

# thank you for the example, anonOstrich/peliloki
def login_required(role="ANY"):    
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            
            unauthorized = False

            if role != "ANY":
                unauthorized = True
            
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
    adminrole = Role("ADMIN")
    editor = Role("EDITOR")
    lang = Role("LANGUAGE_CONSULTANT")
    pic = Role("PICTURE_EDITOR")
    layout = Role("LAYOUT_ARTIST")
    admin_pw = os.environ.get("ADMIN_PW")
    if not admin_pw:
        raise Exception("ADMIN_PW is not set")
    admin = User(username="admin", name="Admin Admin", plaintext_password=admin_pw)
    db.session.add(admin)
    db.session.add_all((adminrole, editor, lang, pic, layout))
    db.session.commit()
    admin_is_admin = UserRole(user_id = admin.id, role_id = adminrole.id)
    admin_is_editor = UserRole(user_id = admin.id, role_id = editor.id)
    admin_is_lang = UserRole(user_id = admin.id, role_id = lang.id)
    admin_is_pic = UserRole(user_id = admin.id, role_id = pic.id)
    admin_is_layout = UserRole(user_id = admin.id, role_id = layout.id)
    db.session.add_all((admin_is_admin, admin_is_editor, admin_is_lang, admin_is_pic, admin_is_layout))
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
