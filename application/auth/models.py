from application import db, os, bcrypt
from application.help import getArticlesWithCondition, getPicturesWithCondition
from application.models import Base
from application.people.models import Name
from application.articles.models import Article
from sqlalchemy.sql import text

class User(Base):

    __tablename__ = "account"

    name = db.Column(db.String(144), nullable=False)
    username = db.Column(db.String(144), nullable=True)
    password = db.Column(db.Binary(60), nullable=True)

    user_roles = db.relationship("UserRole", backref="account", lazy=True)

    names = db.relationship("Name", backref='account', lazy=True)
    articles_writing = db.relationship("Article", foreign_keys=[Article.writer], lazy=True)
    articles_created = db.relationship("Article", foreign_keys=[Article.created_by], lazy=True)
    articles_in_charge_of = db.relationship("Article", foreign_keys=[Article.editor_in_charge], lazy=True)

    def __init__(self, name, username, plaintext_password=None):
        self.name = name
        self.username = username
        if plaintext_password:
            self.password = bcrypt.generate_password_hash(plaintext_password)

# methods required by flask_login
    def get_id(self):
        return self.id

    def is_anonymous(self):
        return False

    def is_active(self):
        return True

    def is_authenticated(self):
        return True
# ----

# role related funtions
# credit partially to anonOstrich/peliloki/

    def roles(self):
        return Role.query.join(Role.user_roles).filter_by(user_id=self.id).all()


    def has_role(self, role_name):
        roles = self.roles()
        for role in roles:
            if role.name == role_name:
                return True
        return False

    # parameters are role objects
    def add_roles(self, *roles):
        def create_user_role(r):
            return UserRole(user_id = self.id, role_id = r.id)
        
        user_roles = map(create_user_role, roles)
        db.session.add_all(user_roles)
        db.session.commit()


    def add_role(self, role):
        self.add_roles(role)

# ----

    def set_password(self, plaintext_password: str) -> bool:
        try:
            self.password = bcrypt.generate_password_hash(plaintext_password)
            db.session().commit()
            return True
        except Exception:
            return False

    def set_editor(self, editor):
        try:
            self.editor = editor
            db.session().commit()
            return True
        except Exception:
            return False

    def is_editor(self):
        return self.editor

    def is_admin(self):
        return self.admin

    def set_name(self, name):
        try:
            self.name = name
            db.session().commit()
            return True
        except Exception:
            return False

    def is_correct_password(self, plaintext_password: str) -> bool:
        if not self.password:
            return False
        return bcrypt.check_password_hash(self.password, plaintext_password)
    
    def add_name(self, name):
        new_name = Name(name, self.id)
        db.session().add(new_name)
        db.session().commit()

    def get_articles_writing(self):
        condition = "(Article.ready = %s AND Article.writer = %d)" % (("false" if os.environ.get("HEROKU") else "0"), self.id)
        return getArticlesWithCondition(condition)

    def get_articles_editing(self):
        condition = "(Article.ready = %s AND Article.editor_in_charge = %d)" % (("false" if os.environ.get("HEROKU") else "0"), self.id)
        return getArticlesWithCondition(condition)

    def get_pictures_responsible(self):
        condition = "Picture.responsible = %d" % self.id
        return getPicturesWithCondition(condition)
    
    def get_articles_language_checking(self):
        condition = "Article.language_consultant = %d" % self.id
        return getArticlesWithCondition(condition)

class UserRole(Base):

    __tablename__ = "userrole"

    user_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable = False)
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"), nullable = False)

    def __init__(self, user_id, role_id):
        self.user_id = user_id
        self.role_id = role_id

class Role(Base):
    __tablename__ = "role"

    name = db.Column(db.String(64), nullable=False, unique=True)
    user_roles = db.relationship("UserRole", backref="role", lazy = True)

    def __init__(self, name):
        self.name = name