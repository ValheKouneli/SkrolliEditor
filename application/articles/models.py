from application import db
from application.help import getArticlesWithCondition
from application.models import Base
from sqlalchemy.sql import text

class Article(Base):

   name = db.Column(db.String(144), nullable=False)
   issue = db.Column(db.Integer, db.ForeignKey('issue.id'), nullable=True)
   pages = db.Column(db.Integer, nullable=True)
   editor_in_charge = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=True)
   editing_status = db.Column(db.Float, nullable=False)
   editing_status_text = db.Column(db.String(144), nullable=True)
   writer = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=True)
   writing_status = db.Column(db.Float, nullable=False)
   writing_status_text = db.Column(db.String(144), nullable=True)
   title = db.Column(db.String(144), nullable=True)
   subtitle = db.Column(db.String(144), nullable=True)
   TOC_text = db.Column(db.String(144), nullable=True)
   language_consultant = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=True)
   lenght_in_chars = db.Column(db.Integer, nullable=True)
   language_consultation_status = db.Column(db.Float, nullable=False)
   language_consultation_status_text = db.Column(db.String(144), nullable=True)
   layout_artist = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=True)
   layout_status = db.Column(db.Float, nullable=False)
   layout_status_text = db.Column(db.String(144), nullable=True)
   ready = db.Column(db.Boolean, nullable=False)

   created_by = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
   synopsis = db.Column(db.Integer, db.ForeignKey('synopsis.id'), nullable=True)


   def __init__(self, name, created_by):
      self.name = name
      self.ready = False
      self.editing_status = 0.0
      self.writing_status = 0.0
      self.language_consultation_status = 0.0
      self.layout_status = 0.0
      self.created_by = created_by

   @staticmethod
   def get_all_articles():
      return getArticlesWithCondition("0=0")

class Synopsis(Base):
   article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)
   content = db.Column(db.String(288), nullable=True)

   def __init__(self, article_id, content):
      self.article_id = article_id
      self.content = content
