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

   person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)

   articles_created = db.relationship("Article", backref='account', lazy=True)

   def __init__(self, name, username, plaintext_password, personid):
       self.name = name
       self.username = username
       self.password = bcrypt.generate_password_hash(plaintext_password)
       self.person_id = personid

   def get_id(self):
       return self.id

   def is_active(self):
       return True

   def is_authenticated(self):
       return True

   def set_password(self, plaintext_password):
      self.password = bcrypt.generate_password_hash(plaintext_password)

   def is_correct_password(self, plaintext_password):
      return bcrypt.check_password_hash(self.password, plaintext_password)