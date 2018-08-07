from application.auth.models import User
from application.people.models import Name

def getPeopleOptions():
    choices = []
    names = Name.query.all()
    for name in names:
        user = User.query.filter_by(id = name.user_id).first()
        choices.append((name.user_id, name.name + ' (' + user.name + ')'))
    print("choises: ", choices)
    return sorted(choices, key=lambda choice: choice[0], reverse=True)
