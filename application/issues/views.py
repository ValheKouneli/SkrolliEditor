from flask import render_template, request, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user

from application import app, db
from application.help import getArticlesWithCondition
from application.articles.forms import ArticleForm
from application.help import getEditorOptions, getIssueOptions, getPeopleOptions
from application.issues.models import Issue

@app.route("/issues/", methods=["GET"])
def issues_index():
    issues = Issue.query.all()
    return render_template("/issues/list.html", issues = issues)

@app.route("/<issue>/articles/", methods=["GET"])
def articles_in_issue(issue):
    try:
        issueid = Issue.query.filter_by(name=issue).first().id
    except:
        return redirect(url_for("error404"))

    return render_template("/articles/list.html",
        issue = issue,
        title = "Articles in " + issue,
        articles=getArticlesWithCondition("issue = "+ str(issueid)))

@app.route("/<issue>/articles/new", methods=["GET"])
@login_required
def articles_create_for_issue(issue):
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
