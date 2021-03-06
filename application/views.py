from flask import render_template, redirect, url_for
from application import app, os
from application.help import getArticlesWithCondition
from application.articles.models import Article
from flask_login import current_user


@app.route("/")
def index():
    if current_user.is_authenticated:
        if current_user.has_role("PICTURE_EDITOR"):
            return redirect(url_for("picture_editor_page"))
        elif current_user.has_role("LANGUAGE_CONSULTANT"):
            return redirect(url_for("language_consultant_page"))

        return redirect(url_for("mypage"))
    else:
        return redirect(url_for("auth_login"))

@app.route("/404/")
def error404():
    return render_template("error404.html")

@app.route("/403/")
def error403():
    return render_template("error403.html")