from application import db
from application.models import Base
from application import bcrypt
from application.people.models import Person
from application.articles.models import Article

class User(Base):

    __tablename__ = "account"

    name = db.Column(db.String(144), nullable=False)
    username = db.Column(db.String(144), nullable=False)
    password = db.Column(db.String(144), nullable=False)
    editor = db.Column(db.Boolean(), nullable=False)

    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=True)

    articles_created = db.relationship("Article", backref='account', lazy=True)

    def __init__(self, name, username, plaintext_password):
        self.name = name
        self.username = username
        self.password = bcrypt.generate_password_hash(plaintext_password)
        self.editor = False

    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def set_password(self, plaintext_password):
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

    def get_editor(self):
        return self.editor

    def set_name(self, name):
        try:
            self.name = name
            db.session().commit()
            return True
        except Exception:
            return False

    def is_correct_password(self, plaintext_password):
        return bcrypt.check_password_hash(self.password, plaintext_password)