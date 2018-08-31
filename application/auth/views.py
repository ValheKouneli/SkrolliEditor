from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user

from application import app, db, login_required
from application.auth.models import User
from application.auth.forms import LoginForm, RegisterForm, UpdateAccountForm
from application.articles.views_helper import update_status, delete_article
from application.pictures.views_helper import update_picture_status, delete_picture
from application.articles.models import Article
from application.pictures.models import Picture
from application.react_to_post_request import react_to_post_request
from application.help import getArticlesWithCondition, getPicturesWithCondition, getPictureWithId


@app.route("/auth/login/", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())

    form = LoginForm(request.form)

    user = User.query.filter_by(username=form.username.data).first()
    if (not user) or (not user.is_correct_password(form.password.data)):
        return render_template("auth/loginform.html", form = form,
                               error = "No such username or password")


    login_user(user)
    next = request.form.get("next_address")
    if next and next != "None": 
        return redirect(next)
    
    return redirect(url_for("index"))

@app.route("/auth/logout/")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/auth/register/", methods = ["GET", "POST"])
def auth_register():
    if request.method == "GET":
        return render_template("auth/registerform.html", form = RegisterForm())

    form = RegisterForm(request.form)

    if not form.validate():
        return render_template("auth/registerform.html", form = form)

    u = User(form.name.data, form.username.data, form.password.data)
    db.session().add(u)
    db.session().commit()
    u.add_name(form.name.data)

    login_user(u)
    return redirect(url_for("index")) 

@app.route("/auth/update/", methods = ["GET", "POST"])
@login_required()
def auth_update():
    if request.method == "GET":
        form = UpdateAccountForm()
        form.name.data = current_user.name
        return render_template("auth/updateaccountform.html", form = form)

    form = UpdateAccountForm(request.form)

    if not form.validate():
        return render_template("auth/updateaccountform.html", form = form)
    
    if (not current_user.is_authenticated) or (not current_user.is_correct_password(form.oldpassword.data)):
        return render_template("auth/updateaccountform.html", form = form,
                               error = "Incorrect password")

    if form.password.data:
        current_user.set_password(form.password.data)
    if current_user.name != form.name.data:
        current_user.add_name(form.name.data)
        current_user.set_name(form.name.data)

    return redirect(url_for("index"))




@app.route("/auth/mypage/", methods = ["GET", "POST"])
@login_required()
def mypage():
    alert = {}
    open = 0

    if request.method == "POST":
        response = react_to_post_request(request, current_user)
        if response["redirect"]:
            return response["redirect"]
        else:
            alert = response["alert"]
            open = response["open"]
            # fall trough

    return render_template("people/tasks.html",
        person_is = "I am",
        posessive_form = "My",
        system_name = current_user.name,
        articles_writing = current_user.get_articles_writing().fetchall(),
        articles_editing = current_user.get_articles_editing().fetchall(),
        pictures_responsible = current_user.get_pictures_responsible().fetchall(),
        articles_language_checking = current_user.get_articles_language_checking().fetchall(),
        open = open,
        alert = alert,
        user_id=current_user.id)

@app.route("/auth/languageconsultant/", methods = ["GET", "POST"])
def language_consultant_page():
    alert = {}

    if request.method == "POST":
        response = react_to_post_request(request, current_user)

        if response["redirect"]:
            return response["redirect"]
        else:
            alert = response["alert"]
            # fall trough

    articles = getArticlesWithCondition(
        "(Article.editing_status = 100" + \
        " AND Article.writing_status = 100" + \
        " AND NOT Article.language_checked" + \
        " AND Article.language_consultant IS NULL)")
    articles = articles.fetchall()

    my_articles = None
    if current_user.is_authenticated:
        my_articles = getArticlesWithCondition(
            "(Article.editing_status = 100" + \
            " AND Article.writing_status = 100" + \
            " AND NOT Article.language_checked" + \
            " AND Article.language_consultant = %s)" % current_user.id)
        my_articles = my_articles.fetchall()

    return render_template("auth/language_consultant_page.html",
        articles = articles,
        my_articles = my_articles,
        current_user = current_user,
        alert = alert)   


@app.route("/auth/pictureeditor/", methods=["GET", "POST"])
def picture_editor_page():
    alert = {}

    if request.method == "POST":
        if not (current_user and
            current_user.has_role("PICTURE_EDITOR")):
            return redirect(url_for("error403"))

        try:
            id = int(request.form["picture_id"])
        except:
            message = "Request to mark picture ready failed, because either" + \
                " parameter picture_id was missing or it was not an integer."
            return render_template("error500.html", message=message)
        
        picture = Picture.query.get(id)
        if not picture:
            return redirect(url_for("error404"))
        picture.ready = True
        db.session.commit()
        alert = {"type": "success",
            "text": "Picture marked ready!" }
        # fall trough

    pictures = getPicturesWithCondition(
        "(Picture.status = 100" + \
        " AND NOT Picture.ready)")
    pictures = pictures.fetchall()

    return render_template("auth/picture_editor_page.html",
        pictures = pictures,
        current_user = current_user,
        alert = alert)
