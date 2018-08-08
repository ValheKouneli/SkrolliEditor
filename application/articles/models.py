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
      query = text(
            "SELECT Article.id AS id, Article.name AS name, Account.name AS writer, Article.ready AS ready FROM Article"
            " LEFT JOIN Account ON Account.id = Article.writer"
            " WHERE (Article.ready = 0)"
            " GROUP BY Article.id"
      )
      res = db.engine.execute(query)
      return db.engine.execute(query)

   @staticmethod
   def get_all_articles():
      query = text(
            "SELECT Article.id AS id, Article.name AS name, Account.name AS writer, Article.ready AS ready FROM Article"
            " LEFT JOIN Account ON Account.id = Article.writer"
            " GROUP BY Article.id"
      )
      return db.engine.execute(query)
