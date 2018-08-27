from flask import redirect, render_template, request, url_for
from application.articles.models import Article, Synopsis
from application.articles.forms import ArticleForm, set_options, set_article_according_to_form
from application import db

def update_status(request, current_user, id):
      if not current_user.editor:
            return None
        
      form = request.form
      article = Article.query.get(id)

      if not article:
            alert = {"type": "danger",
                  "text": "Something went wrong."}
      else:
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


def delete_article(request, current_user, id):
      if not current_user.admin:
            return None
            
      article_to_delete = Article.query.get(id)
      if article_to_delete:
            db.session.delete(article_to_delete)
            synopsis_to_delete = Synopsis.query.filter_by(article_id = id).first()
            if synopsis_to_delete:
                  db.session.delete(synopsis_to_delete)
            db.session.commit()
            alert = {"type": "success",
                  "text": "Article deleted!"}
      else:
            alert = {"type": "danger",
                  "text": "Article was already removed."}
      return alert


def create_article(request, current_user):
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