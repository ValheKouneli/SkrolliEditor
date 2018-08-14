from application import db, os
from application.help import getArticlesWithCondition
from application.models import Base
from application.people.models import Name
from application.articles.models import Article
import bcrypt
from sqlalchemy.sql import text

class User(Base):

    __tablename__ = "account"

    name = db.Column(db.String(144), nullable=False)
    username = db.Column(db.String(144), nullable=True)
    password = db.Column(db.String(144), nullable=True)
    editor = db.Column(db.Boolean(), nullable=False)
    admin = db.Column(db.Boolean(), nullable=False)

    names = db.relationship("Name", backref='account', lazy=True)
    articles_writing = db.relationship("Article", foreign_keys=[Article.writer], lazy=True)
    articles_created = db.relationship("Article", foreign_keys=[Article.created_by], lazy=True)
    articles_in_charge_of = db.relationship("Article", foreign_keys=[Article.editor_in_charge], lazy=True)

    def __init__(self, name, username, plaintext_password):
        self.name = name
        self.username = username
        if plaintext_password:
            self.password = bcrypt.hashpw(bytes(plaintext_password, encoding='utf-8'), bcrypt.gensalt()).decode('utf-8')
        else:
            self.password = ""
        self.editor = False
        self.admin = False

    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def set_password(self, plaintext_password: str) -> bool:
        try:
            self.password = bcrypt.hashpw(plaintext_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
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
        print(bcrypt.hashpw(plaintext_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'))
        print(self.password)
        return bcrypt.hashpw(plaintext_password.encode('utf-8'), self.password.encode('utf-8')).decode('utf-8') == self.password
    
    def add_name(self, name):
        new_name = Name(name, self.id)
        db.session().add(new_name)
        db.session().commit()

    def find_articles_writing(self):
        condition = "(Article.ready = %s AND Article.writer = %d)" % (("false" if os.environ.get("HEROKU") else "0"), self.id)
        return getArticlesWithCondition(condition)

    def find_articles_editing(self):
        condition = "(Article.ready = %s AND Article.editor_in_charge = %d)" % (("false" if os.environ.get("HEROKU") else "0"), self.id)
        return getArticlesWithCondition(condition)
