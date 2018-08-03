from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user

from application import app, db
from application.people.models import Person, Name
from application.people.forms import PersonForm

@app.route("/people/", methods=["GET"])
def people_index():
    return render_template("/people/list.html", people = get_people())

@app.route("/people/new/")
@login_required
def people_form():
    if not current_user.editor:
        return render_template("/people/list.html", people = get_people())

    form = PersonForm()
    return render_template("/people/new.html", form = form)

@app.route("/people/", methods=["POST"])
@login_required
def people_create():
    if not current_user.editor:
        return render_template("/people/list.html", people = get_people())

    form = PersonForm(request.form)

    if not form.validate():
        return render_template("people/new.html", form = form)

    p = Person()
    db.session().add(p)
    db.session().commit()
    p.add_name(form.name.data)

    return redirect(url_for("people_index"))

@app.route("/people/<person_id>/", methods=["GET"])
@login_required
def person_edit(person_id):
    form = PersonForm()
    name = ""
    username = ""
    prsn = Person.query.filter_by(id = person_id).first()

    if prsn.user:
        username = prsn.user.username
        name = prsn.user.name

    names = list(map(lambda name: {"name":name.name, "id":name.id}, prsn.names))
    person = {"id": person_id, "name": name, "username": username, "names": names}

    return render_template("/people/edit.html", person = person, form = form)

@app.route("/people/<person_id>/delete_name/<name_id>", methods=["POST"])
@login_required
def delete_name(name_id, person_id):
    if not current_user.editor:
        return render_template("/people/list.html", people = get_people())

    name_to_delete = Name.query.filter_by(id = name_id).first()
    db.session.delete(name_to_delete)
    db.session.commit()
    return redirect(url_for("person_edit", person_id=person_id))

@app.route("/people/<person_id>", methods=["POST"])
@login_required
def names_create(person_id):
    if not current_user.editor:
        return render_template("/people/list.html", people = get_people())

    form = PersonForm(request.form)

    if not form.validate():
        return render_template("/people/edit.html", person=eval(request.form["person"]), form = form)

    n = Name(form.name.data, person_id)

    db.session().add(n)
    db.session().commit()

    return redirect(url_for("person_edit", person_id=person_id))

def get_people():
    people = []
    ppl = Person.query.all()
    for person in ppl:
        account = ""
        name = ""
        if person.user:
            account = person.user.username
            name = person.user.name
        names = Name.query.filter_by(person_id=person.id)
        people.append({'id': person.id, 'account': account, 'name': name, 'names': names})
    return people