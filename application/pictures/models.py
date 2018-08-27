from application import db
from application.models import Base

class Picture(Base):
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=True)
    description = db.Column(db.String, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    ready = db.Column(db.Boolean, nullable=False)
    responsible = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=True)

    def __init__(self, article_id, description):
        self.article_id = article_id
        self.status = 0
        self.ready = False
        self.description = description