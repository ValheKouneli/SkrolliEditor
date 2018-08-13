from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user

from application import app, db
from application.articles.models import Article, Synopsis
from application.articles.forms import ArticleForm
from application.auth.models import User
from application.help import getArticleWithId, getPeopleOptions, getEditorOptions, getIssueOptions

@app.route("/articles/", methods=["GET"])
def articles_index():
    articles = Article.get_all_articles().fetchall()
    return render_template("/articles/list.html", articles = articles)

@app.route("/articles/new/")
@login_required
def articles_form():
    if not current_user.editor:
        return render_template("articles/list.html")

    form = ArticleForm()
    form.writer.choices = getPeopleOptions()
    form.editorInCharge.choices = getEditorOptions()
    form.issue.choices = getIssueOptions()

    return render_template("/articles/new.html", form=form)

@app.route("/articles/<article_id>/", methods=["POST"])
@login_required
def articles_set_ready(article_id):

    #todo: give redirect address as a parameter
    a = Article.query.get(article_id)
    a.ready = True
    db.session().commit()

    return redirect(url_for("articles_index"))


@app.route("/article/<article_id>/", methods=["GET"])
def show_article(article_id):
    try:
        id = int(article_id)
        print("id: ", id)
    except:
        return redirect(url_for("error404"))
    article = getArticleWithId(id)
    
    if article is None:
        return redirect(url_for("error404"))

    synopsis = ""
    try:
        synopsis = Synopsis.query.filter_by(article_id=id).first().content
    except:
        pass

    return render_template("/articles/article.html", article=article, synopsis=synopsis)

@app.route("/article/<article_id>/delete/", methods=["POST"])
@login_required
def delete_article(article_id):
    if current_user.is_admin:
        try:
            article_to_delete = Article.query.filter_by(id = article_id).first()
            db.session.delete(article_to_delete)
            synopsis_to_delete = Synopsis.query.filter_by(article_id = article_id).first()
            db.session.delete(synopsis_to_delete)
        except:
            pass
        db.session.commit()

    return redirect(url_for("articles_index")) # todo: change this to where the request came from

@app.route("/articles/", methods=["POST"])
@login_required
def articles_create():

    if not current_user.editor:
        return render_template("articles/list.html")

    form = ArticleForm(request.form)
    form.issue.choices = getIssueOptions() # todo: keep old selection
    form.writer.choices = getPeopleOptions() # todo: keep old selection
    form.editorInCharge.choices = getEditorOptions() # todo: keep old selection

    if not form.validate():
        return render_template("articles/new.html", form = form)

    a = Article(form.name.data, current_user.id)
    a.issue = int(form.issue.data)
    a.writer = int(form.writer.data)
    a.editor_in_charge = int(form.editorInCharge.data)

    db.session().add(a)
    db.session().commit()
    
    if len(form.synopsis.data) > 0:
        s = Synopsis(article_id = a.id, content=form.synopsis.data)
        db.session().add(s)
        db.session().commit()
    

    return redirect(url_for("articles_index"))
