from flask import render_template, request, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user

from application import app, db
from application.auth.models import User
from application.auth.forms import LoginForm, RegisterForm, UpdateAccountForm
from application.articles.models import updateStatus


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
        article_id = request.form["article_id"]
        open = article_id
        alert = updateStatus(request=request, current_user=current_user, id=article_id)
        if not alert:
            return redirect(url_for("error403"))

    return render_template("people/tasks.html",
        person_is = "I am",
        posessive_form = "My",
        system_name = current_user.name,
        articles_writing = current_user.get_articles_writing(),
        articles_editing = current_user.get_articles_editing(),
        open = open,
        alert = alert)
