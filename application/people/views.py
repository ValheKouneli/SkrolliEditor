from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user

from application import app, db
from application.people.models import Person, Name
from application.people.forms import NewPersonForm

@app.route("/people/", methods=["GET"])
def people_index():
    people = [{}]
    ppl = Person.query.all()
    for person in ppl:
        account = ""
        name = ""
        if person.user is not null:
            account = person.user.username
            name = person.user.name
        names = Name.query.filter_by(person_id=person.id)
        people.append({'account': account, 'name': name, 'names': names})
    
    return render_template("/people/list.html", people = people)