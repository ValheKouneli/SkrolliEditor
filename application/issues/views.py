from flask import render_template, request, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user

from application import app, db
from application.articles.models import Article
from application.articles.views_helper import update_status, delete_article, create_article
from application.articles.forms import ArticleForm, create_article_form
from application.help import getEditorOptions, getIssueOptions, getPeopleOptions
from application.issues.models import Issue
from application.issues.forms import IssueForm
from application.issues.views_helper import create_new_issue, delete_issue
from application.kanban_page_helper import react_to_post_request

from sqlalchemy.sql import text

@app.route("/issues/", methods=["GET", "POST"])
def issues_index():
    form = IssueForm()
    alert = {}

    if request.method == "POST":
        if request.form.get('create', None):
            create_new_issue(request, current_user)
        elif request.form.get('delete', None):
            delete_issue(request, current_user)


    query = text(
        "SELECT issue.id, issue.name FROM issue ORDER BY issue.name"
    )
    issues = db.engine.execute(query)
    
    return render_template("/issues/list.html",
        current_user = current_user,
        issues = issues,
        form = form,
        alert = alert)



@app.route("/<issue>/articles/", methods=["GET", "POST"])
def articles_in_issue(issue):
    try:
        issueid = Issue.query.filter_by(name=issue).first().id
    except:
        return redirect(url_for("error404"))

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
        planned_articles = Article.get_all_planned_articles(int(issueid)),
        draft_articles = Article.get_all_draft_articles(int(issueid)),
        written_articles = Article.get_all_written_articles(int(issueid)),
        edited_articles = Article.get_all_edited_articles(int(issueid)),
        finished_articles = Article.get_all_finished_articles(int(issueid)),
        alert = alert,
        open = open,
        topic = "Articles " + issue,
        issue = issue)

@app.route("/issues/<id>/", methods=["GET"])
def issue_by_id(id):
    issue = Issue.query.get(id)
    if not issue:
        return redirect(url_for("error404"))
    return redirect(url_for("articles_in_issue", issue=issue.name))

@app.route("/<issue>/articles/new/", methods=["GET", "POST"])
@login_required
def articles_form_for_issue(issue):
    try:
        issueid = Issue.query.filter_by(name=issue).first().id
    except:
        return redirect(url_for("error404"))
    
    if not current_user.editor:
        return redirect(url_for("error403"))

    if request.method == "POST":
        # create a new article
        if request.form.get('create_article', None):
            return create_article(
                current_user=current_user,
                request=request)

    form = create_article_form()
    form.issue.data = issueid

    return render_template("/articles/new.html", form=form)

