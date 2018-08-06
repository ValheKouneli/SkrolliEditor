from application import db
from application.models import Base

from sqlalchemy.sql import text

class Article(Base):

   name = db.Column(db.String(144), nullable=False)
   writer = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=True)
   ready = db.Column(db.Boolean, nullable=False)

   created_by = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)


   def __init__(self, name):
      self.name = name
      self.ready = False

   @staticmethod
   def find_articles_not_ready():
      res = Article.query.filter_by(ready = False)

      response = []
      for row in res:
         response.append({"id":row.id, "name":row.name, "writer":row.writer})

      return response