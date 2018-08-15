from application import db
from application.models import Base
from application.articles.models import Article

class Issue(Base):
    name = db.Column(db.String(144), nullable=False)
    current = db.Column(db.Boolean, nullable=False)

    articles = db.relationship("Article", foreign_keys=[Article.issue], lazy=True)

    def __init__(self, name):
        self.name = name
        self.current = False