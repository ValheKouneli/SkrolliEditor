from flask import render_template
from application import app
from application.articles.models import Article

@app.route("/")
def index():
   return render_template("index.html", unfinished_articles=Article.find_articles_not_ready())
