from application import db
from application import bcrypt

class User(db.Model):

   __tablename__ = "account"

   id = db.Column(db.Integer, primary_key=True)
   date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
   date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

   name = db.Column(db.String(144), nullable=False)
   username = db.Column(db.String(144), nullable=False)
   password = db.Column(db.String(5000), nullable=False)

   articles_created = db.relationship("Article", backref='account', lazy=True)

   def __init__(self, name, username, plaintext_password):
       self.name = name
       self.username = username
       self.password = bcrypt.generate_password_hash(plaintext_password)

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