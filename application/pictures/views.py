from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user

from application import app, db
from application.articles.models import Article
from application.help import getPeopleOptions
from application.pictures.forms import PictureForm, create_picture_form, replicate_picture_form
from application.pictures.models import Picture
from application.auth.models import User

@app.route('/articles/<article_id>/new_picture_commission/', methods=["GET", "POST"])
@login_required
def pictures_form(article_id):
    if not current_user.editor:
        return redirect(url_for("error404"))
    
    try:
        id = int(article_id)
    except:
        return redirect(url_for("error404"))
    article = Article.query.get(id)

    if not article:
        return redirect(url_for("error404"))

    if request.method == "GET":
        form = create_picture_form()

    elif request.method == "POST":
        form = replicate_picture_form(request.form)

        if form.validate:
            p = Picture(id, form.description.data, form.type.data)
            user_id = form.responsible.data
            if user_id:
                user = User.query.get(user_id)
                if user:
                    p.responsible = user_id
            db.session.add(p)
            db.session.commit()
            alert = {"type": "success",
                "text": "Picture commission created!"}
            
            return redirect(url_for("articles_show", article_id=article_id))


    return render_template("pictures/new.html",
        form = form,
        article = article) 

@app.route("/pictures/<picture_id>/", methods=["GET", "POST"])
def picture_update(picture_id):
    return redirect(url_for("index"))