from application import db
from application.models import Base

class Article(Base):

   name = db.Column(db.String(144), nullable=False)
   writer = db.Column(db.String(144), nullable=True)
   ready = db.Column(db.Boolean, nullable=False)

   created_by = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

   def __init__(self, name):
      self.name = name
      self.ready = False
