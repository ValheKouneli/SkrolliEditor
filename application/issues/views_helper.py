from flask import render_template, request, redirect, url_for
from flask_login import current_user

from application import db
from application.articles.models import Article
from application.issues.models import Issue
from application.issues.forms import IssueForm

from sqlalchemy.sql import text


def create_new_issue(request, current_user):
    if not (current_user.is_authenticated and current_user.has_role("EDITOR")):
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
        
    return what_to_render(form, alert)


def delete_issue(request, current_user):
    if not (current_user.is_authenticated and current_user.has_role("ADMIN")):
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

    return what_to_render(form, alert)

def what_to_render(form, alert):
    query = text(
        "SELECT issue.id, issue.name FROM issue ORDER BY issue.name"
    )
    issues = db.engine.execute(query)
    return render_template("/issues/list.html",
        current_user = current_user,
        issues = issues,
        form = form,
        alert = alert)

