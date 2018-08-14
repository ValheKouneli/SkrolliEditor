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


   def __init__(self, name):
      self.name = name
      self.ready = False
      self.editing_status = 0.0
      self.writing_status = 0.0
      self.language_consultation_status = 0.0
      self.layout_status = 0.0

   def set_writer(self, writer_id):
      try:
            self.writer = writer_id
            db.session().commit()
            return True
      except Exception:
            return False

   def set_editor(self, editor_id):
      try:
            if editor_id == 0:
                  self.editor_in_charge = None
            else:
                  self.editor_in_charge = editor_id
            db.session().commit()
            return True
      except Exception:
            return False 

   def set_issue(self, issue_id):
      try:
            if issue_id == 0:
                  self.issue = None
            else:
                  self.issue = issue_id
            db.session().commit()
            return True
      except Exception:
            return False

   def set_name(self, name):
      try:
            self.name = name
            db.session().commit()
            return True
      except Exception:
            return False 


   @staticmethod
   def get_all_articles():
      return getArticlesWithCondition("0=0")
