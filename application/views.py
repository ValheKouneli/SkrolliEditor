from flask import render_template
from application import app
from application.articles.models import Article
from flask_login import current_user

@app.route("/")
def index():
    unfinished_articles = Article.find_articles_not_ready()
    if unfinished_articles.count() > 0:
        return render_template("index.html", unfinished_articles=Article.find_articles_not_ready())
    else:
        return render_template("index.html")
