from flask import render_template, request, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user

from application import app, db
from application.articles.models import Article, updateStatus, deleteArticle
from application.articles.forms import ArticleForm
from application.help import getEditorOptions, getIssueOptions, getPeopleOptions
from application.issues.models import Issue
from application.issues.forms import IssueForm

from sqlalchemy.sql import text

@app.route("/issues/", methods=["GET"])
def issues_index():
    query = text(
        "SELECT issue.id, issue.name FROM issue ORDER BY issue.name"
    )
    issues = db.engine.execute(query)
    return render_template("/issues/list.html", current_user=current_user, issues = issues)

@app.route("/<issue>/articles/", methods=["GET", "POST"])
def articles_in_issue(issue):
    try:
        issueid = Issue.query.filter_by(name=issue).first().id
    except:
        return redirect(url_for("error404"))

    alert = {}
    open = 0

    if request.method == "POST":
        id = request.form["article_id"]
        open = id

        if request.form.get('update_status', None):
            # returns None if user is not authorized
            alert = updateStatus(request=request, current_user=current_user, id=int(id))
            if not alert:
                return redirect(url_for("error403"))

        elif request.form.get('delete', None):
            # returns None if user is not authorized
            alert = deleteArticle(request=request, current_user=current_user, id=int(id))
            if not alert:
                return redirect(url_for("error403"))

    return render_template("articles/editor_view.html", 
        planned_articles = Article.get_all_planned_articles(int(issueid)),
        draft_articles = Article.get_all_draft_articles(int(issueid)),
        written_articles = Article.get_all_written_articles(int(issueid)),
        edited_articles = Article.get_all_edited_articles(int(issueid)),
        finished_articles = Article.get_all_finished_articles(int(issueid)),
        alert = alert,
        open = open,
        topic = "Articles " + issue,
        issue = issue)

@app.route("/issues/<id>", methods=["GET"])
def issue_by_id(id):
    issue = Issue.query.get(id)
    if not issue:
        return redirect(url_for("error404"))
    return redirect(url_for("articles_in_issue", issue=issue.name))

@app.route("/<issue>/articles/new", methods=["GET"])
@login_required
def articles_form_for_issue(issue):
    try:
        issueid = Issue.query.filter_by(name=issue).first().id
    except:
        return redirect(url_for("error404"))
    
    if not current_user.editor:
        return redirect(url_for("error403"))

    form = ArticleForm()
    form.writer.choices = getPeopleOptions()
    form.editorInCharge.choices = getEditorOptions()
    form.issue.choices = getIssueOptions()
    form.issue.data = issueid

    return render_template("/articles/new.html", form=form)

@app.route("/issues/new/", methods=["GET", "POST"])
@login_required
def issues_create():
    if request.method == "GET":
        form = IssueForm()
        return render_template("/issues/new.html", form=form)
    
    if not current_user.editor:
        return redirect(url_for("error403"))

    form = IssueForm(request.form)

    if not form.validate():
        return render_template("issues/new.html", form = form)
    
    issue = Issue(form.name.data)
    db.session.add(issue)
    db.session.commit()

    return redirect(url_for("issues_index"))

@app.route("/<issue_id>/delete", methods=["POST"])
@login_required
def issues_delete(issue_id):
    if not current_user.is_admin:
        return redirect(url_for("error403"))

    issue_to_delete = Issue.query.get(issue_id)
    if not issue_to_delete:
        return redirect(url_for("error404"))

    articles_in_issue = Article.query.filter_by(issue=issue_id)

    # related articles are not distroyed but unassigned
    for article in articles_in_issue:
        article.set_issue(0)

    db.session.delete(issue_to_delete)
    db.session.commit()

    return redirect(url_for("issues_index"))

