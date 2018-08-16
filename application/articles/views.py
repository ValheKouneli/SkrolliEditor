from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user

from application import app, db
from application.articles.models import Article, Synopsis
from application.articles.forms import ArticleForm
from application.auth.models import User
from application.help import getArticleWithId, getArticlesWithCondition, getPeopleOptions, getEditorOptions, getIssueOptions

@app.route("/articles/", methods=["GET"])
def articles_index():
    articles = Article.get_all_articles().fetchall()
    return render_template("/articles/list.html", articles = articles)

@app.route("/articles/new/", methods=["GET"])
@login_required
def articles_form():
    if not current_user.editor:
        return redirect(url_for("error403"))
    
    form = create_article_form()

    return render_template("/articles/new.html", form=form)

@app.route("/articles/set_ready/<article_id>/", methods=["POST"])
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
    print("article: ", article)    
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
        return redirect(url_for("error403"))

    article = Article.query.get(int(article_id))
    if not article:
        return redirect(url_for("error404"))

    # fetch synopsis
    synopsis = Synopsis.query.filter_by(article_id=int(article_id)).first()

    if request.method == "GET":
        # create form
        form = create_article_form()

        # preselect everything according to article's current status
        form.name.data = article.name
        form.writer.data = article.writer if article.writer is not None else 0
        form.issue.data = article.issue if article.issue is not None else 0
        form.editorInCharge.data = article.editor_in_charge if article.editor_in_charge is not None else 0
        if synopsis:
            form.synopsis.data = synopsis.content
        return render_template("articles/new.html", form=form, updating_article=True, article_id=int(article.id))
    
    # get the sent form
    form = replicate_article_form(request.form)

    if not form.validate():
        return render_template("articles/new.html", form = form, updating_article=True, article_id=int(article.id))

    # change article info
    article = set_article_according_to_form(article, form)

    content = form.synopsis.data
    if synopsis and len(content) > 0:
        synopsis.set_content(form.synopsis.data)
    elif synopsis and len(content) == 0:
        db.session.delete(synopsis)
    elif not synopsis and len(content) > 0:
        new_synopsis = Synopsis(article_id=int(article_id), content=form.synopsis.data)
        db.session.add(new_synopsis)
    else:
        pass

    # commit changes
    db.session.commit()

    return redirect(url_for('show_article', article_id=article_id))

  
@app.route("/articles/", methods=["POST"])
@login_required
def articles_create():

    if not current_user.editor:
        return redirect(url_for("error403"))

    form = create_article_form()

    if not form.validate():
        return render_template("articles/new.html", form = form)

    article = Article(form.name.data, current_user.id)
    article = set_article_according_to_form(article, form)

    db.session().add(article)
    db.session().commit()
    
    if len(form.synopsis.data) > 0:
        synopsis = Synopsis(article_id = article.id, content=form.synopsis.data)
        db.session().add(synopsis)
        db.session().commit()
    

    return redirect(url_for("articles_index"))


@app.route("/articles/orphans/", methods=["GET"])
def articles_orphans():
    return render_template("articles/list.html", articles=getArticlesWithCondition("Article.issue IS NULL"))


def create_article_form():
    form = ArticleForm()
    form = set_options(form)
    return form

def replicate_article_form(form):
    replica = ArticleForm(form)
    replica = set_options(replica)
    return replica

def set_options(articleform):
    articleform.writer.choices = getPeopleOptions()
    articleform.editorInCharge.choices = getEditorOptions()
    articleform.issue.choices = getIssueOptions()
    return articleform

def set_article_according_to_form(article, form):
    article.set_name(form.name.data)
    article.set_writer(int(form.writer.data))
    article.set_issue(int(form.issue.data))
    article.set_editor(int(form.editorInCharge.data))
    return article

