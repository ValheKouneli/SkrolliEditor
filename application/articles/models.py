from application import db
from application.models import Base

from sqlalchemy.sql import text

class Article(Base):

   name = db.Column(db.String(144), nullable=False)
   writer = db.Column(db.String(144), nullable=True)
   ready = db.Column(db.Boolean, nullable=False)

   created_by = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

   def __init__(self, name):
      self.name = name
      self.ready = False

   @staticmethod
   def find_articles_not_ready():
      stmt = text(""
         "SELECT Article.id, Article.name, Article.writer FROM Article"
         " WHERE (Article.ready = 0)")
      res = db.engine.execute(stmt)

      response = []
      for row in res:
         response.append({"id":row[0], "name":row[1], "writer":row[2]})

      return response