from application import db, os
from application.help import getArticlesWithCondition
from application.models import Base
from application.articles.forms import ArticleForm, set_options, set_article_according_to_form
from sqlalchemy.sql import text
from flask import redirect, render_template, request, url_for

class Article(Base):

      name = db.Column(db.String(144), nullable=False)
      issue = db.Column(db.Integer, db.ForeignKey('issue.id'), nullable=True)
      pages = db.Column(db.Integer, nullable=True)
      editor_in_charge = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=True)
      editing_status = db.Column(db.Integer, nullable=False)
      writer = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=True)
      writing_status = db.Column(db.Integer, nullable=False)
      language_consultant = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=True)
      lenght_in_chars = db.Column(db.Integer, nullable=True)
      language_consultation_status = db.Column(db.Integer, nullable=False)
      layout_artist = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=True)
      layout_status = db.Column(db.Integer, nullable=False)
      ready = db.Column(db.Boolean, nullable=False)
      created_by = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
      synopsis = db.Column(db.Integer, db.ForeignKey('synopsis.id'), nullable=True)


      def __init__(self, name, created_by):
            self.name = name
            self.ready = False
            self.editing_status = 0
            self.writing_status = 0
            self.language_consultation_status = 0
            self.layout_status = 0
            self.created_by = created_by

      def set_writer(self, writer_id):
            if writer_id == 0:
                  self.writer = None
            else:
                  self.writer = writer_id


      def set_editor(self, editor_id):
            if editor_id == 0:
                  self.editor_in_charge = None
            else:
                  self.editor_in_charge = editor_id

      def set_issue(self, issue_id):
            if issue_id == 0:
                  self.issue = None
            else:
                  self.issue = issue_id

      def set_name(self, name):
            self.name = name


      @staticmethod
      def get_all_articles():
            return getArticlesWithCondition("0=0")

      @staticmethod
      def get_all_planned_articles(issue=0):
            issuecondition = get_issue_condition(issue)
            condition = "Article.writing_status = 0" + issuecondition
            return getArticlesWithCondition(condition)

      @staticmethod
      def get_all_draft_articles(issue=0):
            issuecondition = get_issue_condition(issue)
            condition = "Article.writing_status > 0 AND" + \
                  " Article.writing_status < 100" + issuecondition
            return getArticlesWithCondition(condition)

      @staticmethod
      def get_all_written_articles(issue=0):
            issuecondition = get_issue_condition(issue)
            condition = "Article.writing_status = 100 AND" + \
                  " Article.editing_status < 100" + issuecondition
            return getArticlesWithCondition(condition)

      @staticmethod
      def get_all_edited_articles(issue=0):
            issuecondition = get_issue_condition(issue)
            condition = "article.editing_status = 100 AND" + \
                  " article.writing_status = 100 AND" + \
                  " Article.ready = %s" % ("false" if os.environ.get("HEROKU") else "0") + \
                  issuecondition
            return getArticlesWithCondition(condition)

      @staticmethod
      def get_all_finished_articles(issue=0):
            issuecondition = get_issue_condition(issue)
            condition = "Article.ready = %s" % ("true" if os.environ.get("HEROKU") else "1") + \
                  issuecondition
            return getArticlesWithCondition(condition)

class Synopsis(Base):
      article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)
      content = db.Column(db.String(288), nullable=True)

      def __init__(self, article_id, content):
            self.article_id = article_id
            self.content = content

      def set_content(self, content):
            self.content = content

def get_issue_condition(issue):
      issuecondition = ""
      if issue != 0 and isinstance(issue, int):
            issue = str(issue)
            issuecondition = " AND Article.issue = " + issue
      elif issue == None:
            issuecondition = " AND Article.issue IS NULL"
      return issuecondition
