from application import db
from application.models import Base
from application.articles.models import Article

class Issue(Base):
    name = db.Column(db.String(144), nullable=False)

    articles_writing = db.relationship("Article", foreign_keys=[Article.issue], lazy=True)