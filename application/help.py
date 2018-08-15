from application import db, os
from sqlalchemy.sql import text

def format_as_pair_id_name(options):
    formatted = [(0, None)]
    for item in options:
        formatted.append((item.id, item.name))
    return formatted

def getPeopleOptions():
    query = text(
        "SELECT Account.name AS name, Account.id AS id FROM Account"
        " GROUP BY Account.name, Account.id"
        " ORDER BY Account.name"
    )
    return format_as_pair_id_name(db.engine.execute(query))

def getEditorOptions():
    query = text(
        "SELECT Account.name AS name, Account.id AS id FROM Account"
        " WHERE Account.editor = %s" % ("true" if os.environ.get("HEROKU") else "1") + \
        " GROUP BY Account.name, Account.id"
        " ORDER BY Account.name"
    )
    return format_as_pair_id_name(db.engine.execute(query))

def getIssueOptions():
    query = text(
        "SELECT id, name FROM Issue ORDER BY name"
    )
    return format_as_pair_id_name(db.engine.execute(query))

def getArticlesWithCondition(condition="(0 = 0)"):
    return getArticlesAmountCondition(condition=condition)

# Returns an array of [amount] articles where the condition [condition]
#  is satisfied
def getArticlesAmountCondition(amount=0, condition="(0=0)"):
    howmany = ""
    order = ""
    if amount > 0:
        howmany = " LIMIT %d" % int(amount)
    if amount != 1:
        order = " ORDER BY Issue.name"
    query = text(
        "SELECT Article.id AS id, Issue.name AS issue,"
        " Article.writing_status AS writing_status,"
        " Article.editing_status AS editing_status,"
        " Article.ready AS ready, Article.name AS name,"
        " Writer.name AS writer, Editor.name AS editor_in_charge FROM Article"
        " LEFT JOIN Account Writer ON Article.writer = Writer.id"
        " LEFT JOIN Account Editor ON Article.editor_in_charge = Editor.id"
        " LEFT JOIN Issue ON Article.issue = Issue.id"
        " WHERE %s" % condition +\
        " GROUP BY Article.id, Article.ready, Article.name, Issue.name, Writer.name, Editor.name" + \
        howmany + order
    )
    return db.engine.execute(query)

def getArticleWithId(id):
    resultArray = getArticlesAmountCondition(amount=1, condition="Article.id = %d" % id)
    try:
        return resultArray.first()
    except:
        return None
        