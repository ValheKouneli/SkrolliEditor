from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user

from application import app, db
from application.issues.models import Issue

@app.route("/issues/", methods=["GET"])
def issues_index():
    issues = Issue.query.all()
    return render_template("/issues/list.html", issues = issues)