from flask import render_template, request, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user

from application import app, db
from application.auth.models import User
from application.auth.forms import LoginForm, RegisterForm, UpdateAccountForm
from application.articles.views_helper import update_status, delete_article
from application.pictures.views_helper import update_picture_status, delete_picture
from application.articles.models import Article


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
@login_required
def auth_update():
    if request.method == "GET":
        form = UpdateAccountForm()
        form.name.data = current_user.name
        return render_template("auth/updateaccountform.html", form = form)

    form = UpdateAccountForm(request.form)

    if not form.validate():
        return render_template("auth/updateaccountform.html", form = form)
    
    if (not current_user) or (not current_user.is_correct_password(form.oldpassword.data)):
        return render_template("auth/updateaccountform.html", form = form,
                               error = "Incorrect password")

    if form.password.data:
        current_user.set_password(form.password.data)
    if current_user.name != form.name.data:
        current_user.add_name(form.name.data)
        current_user.set_name(form.name.data)

    return redirect(url_for("index"))




@app.route("/auth/mypage/", methods = ["GET", "POST"])
@login_required
def mypage():
    alert = {}
    open = 0

    if request.method == "POST":
        # if request is related to an artile, fetch the article
        if (request.form.get('update_status', None) or
            request.form.get('delete', None)):

            try:
                id = int(request.form["article_id"])
            except:
                message = "Article status update or delete request did not contain parameter 'article_id'."
                return render_template("error500.html", message=message)
            article = Article.query.get(id)
            if not article:
                return redirect(url_for("error404"))

            if request.form.get('update_status', None):
                # returns None if user is not authorized
                alert = update_status(request, article, current_user)
                if not alert:
                    return redirect(url_for("error403"))
                try:
                    open = request.form["article_id"]
                except:
                    open = 0
                # FALL THROUGH

            elif request.form.get('delete', None):
                alert = delete_article(request, article, current_user)
                if not alert:
                    return redirect(url_for("error403"))

        elif request.form.get('delete_picture', None):
            # returns None if user is not authorized
            alert = delete_picture(request, current_user)
            if not alert:
                return redirect(url_for("error403"))
            # FALL THROUGH

        elif request.form.get('update_picture_status', None):
            # returns None if user is not authorized
            alert = update_picture_status(request, current_user)
            if not alert:
                return redirect(url_for("error403"))
            try:
                open = request.form["picture_id"]
            except:
                open = 0
            # FALL THROUGH

    return render_template("people/tasks.html",
        person_is = "I am",
        posessive_form = "My",
        system_name = current_user.name,
        articles_writing = current_user.get_articles_writing().fetchall(),
        articles_editing = current_user.get_articles_editing().fetchall(),
        pictures_responsible = current_user.get_pictures_responsible().fetchall(),
        open = open,
        alert = alert)
