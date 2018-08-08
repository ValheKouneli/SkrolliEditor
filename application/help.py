from application import db
from sqlalchemy.sql import text

def sort_and_format(people):
    options = sorted(people, key=lambda person: person["alias"])
    formatted = [(0, None)]
    for item in options:
        formatted.append((item.id, item.alias + " (" + item.name + ")"))
    return formatted

def getPeopleOptions():
    query = text(
        "SELECT Name.name AS alias, Account.name AS name, Account.id AS id FROM Name"
        " LEFT JOIN Account ON Account.id = Name.user_id"
        " GROUP BY Name.id"
    )
    return sort_and_format(db.engine.execute(query))

def getEditorOptions():
    query = text(
        "SELECT Name.name AS alias, Account.name AS name, Account.id AS id FROM Name"
        " LEFT JOIN Account ON Account.id = Name.user_id"
        " WHERE Account.editor = 1"
        " GROUP BY Name.id"
    )
    return sort_and_format(db.engine.execute(query))

def getArticlesWithCondition(condition="(0 = 0)"):
    query = text(
            "SELECT Article.id AS id, Article.ready AS ready, Article.name AS name, Writer.name AS writer, Editor.name AS editor_in_charge FROM Article"
            " LEFT JOIN Account Writer ON Article.writer = Writer.id"
            " LEFT JOIN Account Editor ON Article.editor_in_charge = Editor.id"
            " WHERE %s" % condition +\
            " GROUP BY Article.id"
    )
    return db.engine.execute(query)
