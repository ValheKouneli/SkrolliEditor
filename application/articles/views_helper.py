from flask import redirect, render_template, request, url_for
from application.articles.models import Article, Synopsis
from application.pictures.models import Picture
from application.articles.forms import ArticleForm, set_options, set_article_according_to_form
from application import db

def update_status(request, article, current_user):
      if not (current_user and
            current_user.has_role("EDITOR")):
            
            return None
      form = request.form

      if form["writing_status"] is not None:
            article.writing_status = int(form["writing_status"])
      if form["editing_status"] is not None:
            if int(form["editing_status"]) <= article.writing_status:
                  article.editing_status = int(form["editing_status"])
                  alert = {"type": "success",
                        "text": "Status updated!"}
            else:
                  alert = {"type": "danger",
                        "text": "Editing can not be ahead of writing!"}
      db.session.commit()

      return alert


def delete_article(request, article, current_user):
      if not (current_user and
            current_user.has_role("ADMIN")):

            return None
            
      db.session.delete(article)
      synopsis_to_delete = Synopsis.query.filter_by(article_id = article.id).first()
      if synopsis_to_delete:
            db.session.delete(synopsis_to_delete)
      pictures = Picture.query.filter_by(article_id = article.id)

      for picture in pictures:
            db.session.delete(picture)
      
      db.session.commit()
      alert = {"type": "success",
            "text": "Article deleted!"}

      return alert


def create_article(request, current_user):
      if not (current_user and
            current_user.has_role("EDITOR")):
            
            return None

      redirect_to = None

      if request.form.get('redirect_to', None):
            redirect_to = request.form["redirect_to"]
                
      form = ArticleForm(request.form)
      form = set_options(form)

      if not form.validate():
            return render_template("articles/new.html", \
                  form = form, redirect_to=redirect_to)

      # default redirect address for new article is the page
      # showing all articles for the same issue
      if not redirect_to:
            if form.issue.data:
                  redirect_to = url_for('issue_by_id', id=form.issue.data)
            else:
                  redirect_to = url_for('articles_orphans')

      article = Article(form.name.data, current_user.id)
      article = set_article_according_to_form(article, form)

      db.session().add(article)
      db.session().commit()
    
      if len(form.synopsis.data) > 0:
            synopsis = Synopsis(article_id = article.id, content=form.synopsis.data)
            db.session().add(synopsis)
            db.session().commit()
    
      return redirect(redirect_to)