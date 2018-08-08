from application import db
from application.models import Base
from sqlalchemy.sql import text

class Article(Base):

   name = db.Column(db.String(144), nullable=False)
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


   def __init__(self, name):
      self.name = name
      self.ready = False
      self.editing_status = 0.0
      self.writing_status = 0.0
      self.language_consultation_status = 0.0
      self.layout_status = 0.0

   @staticmethod
   def find_articles_not_ready():
      query = text(
            "SELECT Article.id AS id, Article.name AS name, Writer.name AS writer, Editor.name AS editor_in_charge FROM Article"
            " LEFT JOIN Account Writer ON Article.writer = Writer.id"
            " LEFT JOIN Account Editor ON Article.editor_in_charge = Editor.id"
            " WHERE Article.ready = 0"
      )
      return db.engine.execute(query)

   @staticmethod
   def get_all_articles():
      query = text(
            "SELECT Article.id AS id, Article.name AS name, Writer.name AS writer, Editor.name AS editor_in_charge FROM Article"
            " LEFT JOIN Account Writer ON Article.writer = Writer.id"
            " LEFT JOIN Account Editor ON Article.editor_in_charge = Editor.id"
      )
      return db.engine.execute(query)
