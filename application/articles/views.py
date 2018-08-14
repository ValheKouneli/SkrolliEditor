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

  
@app.route("/article/<article_id>/update/", methods=["GET", "POST"])
@login_required
def article_update(article_id):
    if not current_user.is_editor:
        return redirect(url_for("articles_index")) # todo: create an 'unauthenticated' page

    article = Article.query.get(int(article_id))
    if not article:
        return redirect(url_for("error404"))

    synopsises = Synopsis.query.filter_by(article_id=int(article_id))

    if request.method == "GET":
        # create form
        form = ArticleForm()
        form.writer.choices = getPeopleOptions()
        form.editorInCharge.choices = getEditorOptions()
        form.issue.choices = getIssueOptions()

        # preselect everything according to article's current status
        form.name.data = article.name
        form.writer.data = article.writer if article.writer is not None else 0
        form.issue.data = article.issue if article.issue is not None else 0
        form.editorInCharge.data = article.editor_in_charge if article.editor_in_charge is not None else 0
        try:
            form.synopsis.data = synopsises.first().content
        except:
            pass
        return render_template("articles/new.html", form=form, updating_article=True, article_id=int(article.id))
    
    # create form and preselect eveything according to what was selected when form was sent
    form = ArticleForm(request.form)
    form.writer.choices = getPeopleOptions()
    form.editorInCharge.choices = getEditorOptions()
    form.issue.choices = getIssueOptions()

    if not form.validate():
        return render_template("articles/new.html", form = form, updating_article=True, article_id=int(article.id))

    # change article info it it was changed
    if form.writer.data is not article.writer:
        article.set_writer(form.writer.data)
    if form.issue.data is not article.issue:
        article.set_issue(form.issue.data)
    if form.editorInCharge.data is not article.editor_in_charge:
        article.set_editor(form.editorInCharge.data)

    try:
        synopsis = synopsises.first()
        if synopsis and len(form.synopsis.data) > 0:
            synopsis.set_content(form.synopsis.data)
        elif synopsis and len(form.synopsis.data) == 0:
            db.session.delete(synopsis)
            db.session.commit()
        else:
            new_synopsis = Synopsis(article_id=int(article_id), content=form.synopsis.data)
            db.session.add(new_synopsis)
            db.session.commit()
    except:
        new_synopsis = Synopsis(article_id=int(article_id), content=form.synopsis.data)
        db.session.add(new_synopsis)
        db.session.commit()

    return redirect(url_for('show_article', article_id=article_id))

  
@app.route("/articles/", methods=["POST"])
@login_required
def articles_create():

    if not current_user.editor:
        return render_template("articles/list.html")

    form = ArticleForm(request.form)
    form.writer.choices = getPeopleOptions()
    form.editorInCharge.choices = getEditorOptions()
    form.issue.choices = getIssueOptions()

    if not form.validate():
        return render_template("articles/new.html", form = form)

    a = Article(form.name.data, current_user.id)
    if form.issue.data != 0:
        a.issue = int(form.issue.data)
    if form.writer.data != 0:
        a.writer = int(form.writer.data)
    if form.editorInCharge.data != 0:
        a.editor_in_charge = int(form.editorInCharge.data)

    db.session().add(a)
    db.session().commit()
    
    if len(form.synopsis.data) > 0:
        s = Synopsis(article_id = a.id, content=form.synopsis.data)
        db.session().add(s)
        db.session().commit()
    

    return redirect(url_for("articles_index"))
