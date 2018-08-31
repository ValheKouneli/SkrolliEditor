from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user

from application import app, db
from application.articles.models import Article
from application.help import getPeopleOptions, getPicturesWithCondition
from application.pictures.forms import PictureForm, create_picture_form, replicate_picture_form
from application.pictures.models import Picture
from application.pictures.views_helper import show_prefilled_form, update_picture
from application.auth.models import User
from application.react_to_post_request import react_to_post_request

@app.route('/pictures/', methods=["GET", "POST"])
def pictures_index():
    alert = {}
    open = 0

    if request.method == "POST":
        response = react_to_post_request(request, current_user)
        if response["redirect"]:
            return response["redirect"]
        else:
            alert = response["alert"]
            open = response["open"]
            # fall through

    pictures = getPicturesWithCondition("0=0").fetchall()

    return render_template("pictures/list.html",
        pictures=pictures,
        alert = alert,
        open = open)

@app.route('/pictures/new_picture_commission_for/<article_id>/', methods=["GET", "POST"])
@login_required
def pictures_form(article_id):
    print("HERE")
    if not current_user.editor:
        return redirect(url_for("error404"))
    
    try:
        id = int(article_id)
    except:
        return redirect(url_for("error404"))
    article = Article.query.get(id)

    if not article:
        return redirect(url_for("error404"))

    if request.method == "POST":
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

            print("HERE2")
            
            return redirect(url_for("articles_show", article_id=article_id))

    elif request.method == "GET":
        form = create_picture_form()

        return render_template("pictures/new.html",
            form = form,
            article = article) 

@app.route("/pictures/<picture_id>/update", methods=["GET", "POST"])
@login_required
def picture_update(picture_id):
    # check that user is authorized
    if not current_user.editor:
        return redirect(url_for("error403"))

    # check that parameters are valid
    try:
        id = int(picture_id)
    except:
        return redirect(url_for("error404"))

    # check that id matches a picture
    picture = Picture.query.get(id)
    if not picture:
        return redirect(url_for("error404"))

    # get the article this picture is for
    article = None
    if picture.article_id:
        article = Article.query.get(picture.article_id)

    # show the update form
    if request.method == "GET":
        return show_prefilled_form(picture, article, request)
    # update the picture and redirect
    else:
        return update_picture(picture, article, request)