from flask import redirect, render_template, request, url_for
from flask_login import current_user

from application import app, db, login_required
from application.articles.views_helper import create_article
from application.articles.forms import create_article_form
from application.articles.models import Article
from application.auth.models import User, Role, UserRole
from application.people.models import Name
from application.people.forms import NameForm, AliasForm
from application.react_to_post_request import react_to_post_request

@app.route("/people/", methods=["GET", "POST"])
def people_index():
    form = NameForm()
    alert = {}

    if request.method == "POST":

        # if request is related to an existing User, fetch user
        if (request.form.get('delete', None) or 
            request.form.get('make_editor', None) or
            request.form.get('remove_editor', None)):

            try:
                id = int(request.form['id'])
            except:
                message = "User related request did not contain required parameter id (int)."
                return render_template("error500.html", message=message)

            user = User.query.get(id)

        # request is to create new dummy user
        if request.form.get('create_dummy_user', None):
            if not (current_user and current_user.has_role("EDITOR")):
                return redirect(url_for("error403"))
            
            form = NameForm(request.form)

            if form.validate():
                u = User(form.name.data, "", "")
                db.session().add(u)
                db.session().commit()
                u.add_name(form.name.data)
                # empty form
                form = NameForm(formdata=None)

                alert = {"type": "success",
                    "text": "New dummy user created!"}
            # fall through
        
        # request is to delete user
        elif request.form.get('delete', None):
            if not (current_user and current_user.has_role("ADMIN")):
                return redirect(url_for("error403"))

            if user:
                names = Name.query.filter_by(user_id = id)
                roles = UserRole.query.filter_by(user_id = id)
                for name in names:
                    db.session.delete(name)
                for role in roles:
                    db.session.delte(role)
                db.session.delete(user) 
                db.session.commit()
                alert = {"type": "success",
                    "text": "User succesfully deleted!"}
            else:
                alert = {"type": "danger",
                    "text": "Somebody already deleted that user."}
            # fall through
            
        # request is to make user editor
        elif request.form.get('make_editor', None):
            if not (current_user and current_user.has_role("ADMIN")):
                return redirect(url_for("error403"))

            if not user:
                alert = {"type": "danger",
                    "text": "User was deleted."}
            else:
                editor = Role.query.filter_by(name="EDITOR").first()
                if not editor:
                    message = "There is no role 'EDITOR' in the database!"
                    return render_template("error500.html", message=message)
                user.add_role(editor)
                alert = {"type": "success",
                    "text": "User %s is now editor!" % user.name}
            # fall through

        # request is to make user not-editor
        elif request.form.get('remove_editor', None):
            if not (current_user and current_user.has_role("ADMIN")):
                return redirect(url_for("error403"))

            if not user:
                alert = {"type": "danger",
                    "text": "User was deleted."}
            else:
                editor = Role.query.filter_by(name="EDITOR").first()
                if not editor:
                    message = "There is no role 'EDITOR' in the database!"
                    return render_template("error500.html", message=message)
                editor_roles = UserRole.query.filter_by(user_id = user.id, role_id = editor.id)
                for role in editor_roles:
                    db.session.delete(role)

                articles = Article.query.filter_by(editor_in_charge = id)
                for article in articles:
                    article.editor_in_charge = None
                db.session.commit()
                alert = {"type": "success",
                    "text": "User %s is no longer editor!" % user.name}
                # fall through

            
    return render_template("/people/list.html",
        people = get_people(),
        form = form,
        alert = alert)




@app.route("/people/<user_id>/edit", methods=["GET", "POST"])
@login_required(role="EDITOR")
def person_edit(user_id):

    alert = {}
    form = AliasForm()
    
    if request.method == "POST":

        form = AliasForm(request.form)

        if form.validate():
            name = Name(form.name.data, user_id)

            db.session().add(name)
            db.session().commit()
            # empty form
            form = AliasForm(formdata=None)
            
            alert = {"type": "success",
                "text": "New alias added!"}


    prsn = User.query.get(int(user_id))

    if not prsn:
        return redirect(url_for("error404"))
    
    username = prsn.username
    name = prsn.name

    names = list(map(lambda name: {"name":name.name, "id":name.id}, prsn.names))
    person = {"id": user_id, "name": name, "username": username, "names": names}

    return render_template("/people/edit.html",
        person = person,
        form = form,
        alert = alert)




@app.route("/people/<user_id>/delete_name/<name_id>", methods=["POST"])
@login_required(role="EDITOR")
def delete_name(name_id, user_id):
    name_to_delete = Name.query.filter_by(id = name_id).first()
    db.session.delete(name_to_delete)
    db.session.commit()
    return redirect(url_for("person_edit", user_id=user_id))


@app.route("/people/<user_id>/", methods=["GET", "POST"])
def show_tasks(user_id):
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

    user = User.query.get(int(user_id))
    if not user:
        return redirect(url_for("error404"))
    
    name = user.name

    articles_writing = user.get_articles_writing().fetchall()
    articles_editing = user.get_articles_editing().fetchall()
    pictures_responsible = user.get_pictures_responsible().fetchall()
    articles_language_checking = user.get_articles_language_checking().fetchall()

    return render_template("people/tasks.html",
        articles_writing = articles_writing,
        articles_editing = articles_editing,
        pictures_responsible = pictures_responsible,
        articles_language_checking = articles_language_checking,
        posessive_form = "" + name + "'s",
        system_name = user.name,
        person_is = name + " is",
        user_id=user.id)

@app.route("/people/<user_id>/new_article/", methods=["GET", "POST"])
@login_required(role="EDITOR")
def new_article_for_writer(user_id):
    try:
        id = int(user_id)
    except:
        message = "Provided user id is not a number."
        return render_template("error500.html", message=message)
    user = User.query.get(id)
    
    if not user:
        return redirect(url_for("error404"))

    if request.method == "POST":
        # create a new article
        if request.form.get('create_article', None):
            return create_article(
                current_user=current_user,
                request=request)
    
    form = create_article_form()
    form.writer.data = id
    redirect_to = request.referrer

    return render_template("/articles/new.html",
        form=form,
        redirect_to = redirect_to)


def get_people():
    people = []
    ppl = User.query.all()
    for person in ppl:
        username = ""
        name = person.name
        if person.username:
            username = person.username
        names = Name.query.filter_by(user_id=person.id)
        people.append({'person': person, 'names': names})
    return people