from application import db
from application.models import Base

class Name(Base):

    __tablename__ = "name"

    name = db.Column(db.String(144), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id