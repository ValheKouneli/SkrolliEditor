from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user

from application import app, db
from application.help import getArticlesWithCondition
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
        title = "Articles in " + issue,
        articles=getArticlesWithCondition("issue = "+ str(issueid)))

@app.route("/<issue>/articles/new", methods=["GET"])
def articles_create_for_issue(issue):
    try:
        issueid = Issue.query.filter_by(name=issue).first().id
    except:
        return redirect(url_for("error404"))
    
    return redirect(url_for("articles_create", issue=issueid))
