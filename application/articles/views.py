from flask import redirect, render_template, request, url_for
from flask_login import current_user

from application import app, db, login_required
from application.articles.models import Article, Synopsis
from application.articles.views_helper import update_status, delete_article, create_article
from application.articles.forms import ArticleForm, create_article_form, \
    set_article_according_to_form, replicate_article_form
from application.auth.models import User
from application.pictures.views_helper import update_picture_status, delete_picture
from application.help import getArticleWithId, getArticlesWithCondition, \
    getPeopleOptions, getEditorOptions, getIssueOptions, getPicturesForArticle
from application.kanban_page_helper import react_to_post_request



@app.route("/articles/", methods=["GET", "POST"])
def articles_index():
    alert = {}
    open = 0

    if request.method == "POST":
        response = react_to_post_request(request, current_user)

        if response["redirect"]:
            return response["redirect"]
        else:
            alert = response["alert"]
            open = response["open"]
            # fall trough

    # show all articles
    return render_template("articles/editor_view.html", 
        planned_articles = Article.get_all_planned_articles(),
        draft_articles = Article.get_all_draft_articles(),
        written_articles = Article.get_all_written_articles(),
        edited_articles = Article.get_all_edited_articles(),
        finished_articles = Article.get_all_finished_articles(),
        alert = alert,
        open = open,
        topic = "All articles")

@app.route("/articles/<article_id>/", methods=["GET", "POST"])
def articles_show(article_id):
    alert = {}
    try:
        id = int(article_id)
    except:
        return redirect(url_for("error404"))

    article = Article.query.get(id)
    if not article:
        return redirect(url_for("error404"))

    if request.method == "POST":
        if not current_user and current_user.has_role("EDITOR"):
            return redirect(url_for("error403"))

        if request.form.get('update_status', None):
            # returns None if user is not authorized
            alert = update_status(request, article, current_user)
            if not alert:
                return redirect(url_for("error403"))
            # FALL THROUGH

        elif request.form.get('update_picture_status', None):
            # returns None if user is not authorized
            alert = update_picture_status(request, current_user)
            if not alert:
                return redirect(url_for("error403"))
            # FALL THROUGH

        elif request.form.get('delete_picture', None):
            # returns None if user is not authorized
            alert = delete_picture(request, current_user)
            if not alert:
                return redirect(url_for("error403"))
            # FALL THROUGH

        elif request.form.get('delete', None):
            alert = delete_article(request, article, current_user)
            if not alert:
                return redirect(url_for("error403"))
            if article.issue:
                return redirect(url_for("issue_by_id", id=article.issue))
            else:
                return redirect(url_for("articles_orphans"))


    article = getArticleWithId(int(article_id))
    if not article:
        return redirect(url_for("error404"))
    pictures = getPicturesForArticle(int(article_id)).fetchall()
    
    return render_template("articles/article.html",
        article=article,
        pictures=pictures,
        current_user=current_user,
        alert = alert)


@app.route("/articles/new/", methods=["GET", "POST"])
@login_required(role="EDITOR")
def articles_form():
    if request.method == "POST":

        # create a new article
        if request.form.get('create_article', None):
    
            return create_article(
                current_user=current_user,
                request=request)

    form = create_article_form()

    return render_template("/articles/new.html", form=form)




@app.route("/article/<article_id>/update/", methods=["GET", "POST"])
@login_required(role="EDITOR")
def article_update(article_id):

    article = Article.query.get(int(article_id))
    if not article:
        return redirect(url_for("error404"))

    # fetch synopsis
    synopsis = Synopsis.query.filter_by(article_id=int(article_id)).first()



    if request.method == "GET":
        redirect_to = request.referrer
        # create form
        form = create_article_form()

        # preselect everything according to article's current status
        form.name.data = article.name
        form.writer.data = article.writer if article.writer is not None else 0
        form.issue.data = article.issue if article.issue is not None else 0
        form.editorInCharge.data = \
            article.editor_in_charge if article.editor_in_charge is not None else 0
        if synopsis:
            form.synopsis.data = synopsis.content
        return render_template("articles/new.html",
            form=form, updating_article=True, \
            article_id=int(article.id), redirect_to=redirect_to)
    
    # request method is POST
    
    redirect_to = url_for('articles_index')
    if request.form.get('redirect_to', None):
        redirect_to = request.form["redirect_to"]

    # get the sent form
    form = replicate_article_form(request.form)

    if not form.validate():
        return render_template("articles/new.html", \
            form=form, updating_article=True, \
            article_id=int(article.id), redirect_to=redirect_to)

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

    return redirect(redirect_to)





@app.route("/articles/orphans/", methods=["GET", "POST"])
def articles_orphans():
    alert = {}
    open = 0

    if request.method == "POST":
        response = react_to_post_request(request, current_user)

        if response["redirect"]:
            return response["redirect"]
        else:
            alert = response["alert"]
            open = response["open"]
            # fall trough

    return render_template("articles/editor_view.html", 
        planned_articles = Article.get_all_planned_articles(None),
        draft_articles = Article.get_all_draft_articles(None),
        written_articles = Article.get_all_written_articles(None),
        edited_articles = Article.get_all_edited_articles(None),
        finished_articles = Article.get_all_finished_articles(None),
        alert = alert,
        open = open,
        topic = "Orphan articles",
        redirect_to = url_for('articles_orphans'))
