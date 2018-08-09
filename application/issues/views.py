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
        redirect(url_for("error404"))

    return render_template("/articles/list.html", articles=getArticlesWithCondition("issue = "+ str(issueid)))
