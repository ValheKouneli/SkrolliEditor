from application import db
from application.models import Base

class Person(Base):

    __tablename__ = "person"

    names = db.relationship("Name", backref="person", lazy=True)
    user = db.relationship("User", backref="user", lazy=True, uselist=False)

    def __init__(self):
        i = 1

    def add_name(self, name):
        new_name = Name(name, self.id)
        db.session().add(new_name)
        db.session().commit()

class Name(Base):

    __tablename__ = "name"

    name = db.Column(db.String(144), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)

    def __init__(self, name, person_id):
        self.name = name
        self.person_id = person_id