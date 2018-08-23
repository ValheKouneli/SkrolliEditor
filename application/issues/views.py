from flask import render_template, request, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user

from application import app, db
from application.articles.models import Article, updateStatus, deleteArticle
from application.articles.forms import ArticleForm
from application.help import getEditorOptions, getIssueOptions, getPeopleOptions
from application.issues.models import Issue
from application.issues.forms import IssueForm

from sqlalchemy.sql import text

@app.route("/issues/", methods=["GET", "POST"])
def issues_index():
    form = IssueForm()
    alert = {}

    if request.method == "POST":

        # create new issue
        if request.form.get('create', None):
            if not current_user.editor:
                return redirect(url_for("error403"))

            form = IssueForm(request.form)

            if form.validate():
                issue = Issue(form.name.data)
                db.session.add(issue)
                db.session.commit()
                # empty form
                form = IssueForm(formdata=None)
                alert = {"type": "success",
                    "text": "New issue added to database!"}

        # delete issue
        elif request.form.get('delete', None):
            if not current_user.admin:
                return redirect(url_for("error403"))
            id = request.form["delete"]
            issue_to_delete = Issue.query.get(int(id))
            if not issue_to_delete:
                alert = {"type": "danger",
                    "text": "Issue was already deleted."}
            else:
                articles_in_issue = Article.query.filter_by(issue=id)

                # related articles are not distroyed but made orphans
                for article in articles_in_issue:
                    article.set_issue(0)

                db.session.delete(issue_to_delete)
                db.session.commit()
                alert = {"type": "success",
                    "text": "Issue deleted succesfully!"}


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

