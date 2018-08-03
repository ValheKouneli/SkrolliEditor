from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user

from application import app, db
from application.auth.models import User
from application.people.models import Name
from application.people.forms import NameForm

@app.route("/people/", methods=["GET"])
def people_index():
    return render_template("/people/list.html", people = get_people())

@app.route("/people/new/")
@login_required
def people_form():
    if not current_user.editor:
        return render_template("/people/list.html", people = get_people())

    form = NameForm()
    return render_template("/people/new.html", form = form)

@app.route("/people/", methods=["POST"])
@login_required
def people_create():
    if not current_user.editor:
        return render_template("/people/list.html", people = get_people())

    form = NameForm(request.form)

    if not form.validate():
        return render_template("people/new.html", form = form)

    u = User(form.name.data, 0, 0)
    db.session().add(u)
    db.session().commit()
    u.add_name(form.name.data)

    return redirect(url_for("people_index"))

@app.route("/people/<user_id>/", methods=["GET"])
@login_required
def person_edit(user_id):
    form = NameForm()
    name = ""
    username = ""
    prsn = User.query.filter_by(id = user_id).first()

    username = ""
    if prsn.username:
        username = prsn.username

    name = prsn.name

    names = list(map(lambda name: {"name":name.name, "id":name.id}, prsn.names))
    person = {"id": user_id, "name": name, "username": username, "names": names}

    return render_template("/people/edit.html", person = person, form = form)

@app.route("/people/<user_id>/delete_name/<name_id>", methods=["POST"])
@login_required
def delete_name(name_id, user_id):
    if not current_user.editor:
        return render_template("/people/list.html", people = get_people())

    name_to_delete = Name.query.filter_by(id = name_id).first()
    db.session.delete(name_to_delete)
    db.session.commit()
    return redirect(url_for("person_edit", user_id=user_id))

@app.route("/people/<user_id>", methods=["POST"])
@login_required
def names_create(user_id):
    if not current_user.editor:
        return render_template("/people/list.html", people = get_people())

    form = NameForm(request.form)

    if not form.validate():
        return render_template("/people/edit.html", person=eval(request.form["person"]), form = form)

    n = Name(form.name.data, user_id)

    db.session().add(n)
    db.session().commit()

    return redirect(url_for("person_edit", user_id=user_id))

def get_people():
    people = []
    ppl = User.query.all()
    for person in ppl:
        username = ""
        name = person.name
        if person.username:
            username = person.username
        names = Name.query.filter_by(user_id=person.id)
        people.append({'id': person.id, 'username': username, 'name': name, 'names': names})
    return people