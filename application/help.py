from application import db, os
from sqlalchemy.sql import text

def format_as_pair_id_name_and_alphabetize(query_result):
    options = sorted(query_result, key=lambda option: option["name"])
    formatted = [(0, None)]
    for item in options:
        formatted.append((item.id, item.name))
    return formatted

def getPeopleOptions():
    query = text(
        "SELECT Account.name AS name, Account.id AS id FROM Account"
        " GROUP BY Account.name, Account.id"
    )
    return format_as_pair_id_name_and_alphabetize(db.engine.execute(query))

def getEditorOptions():
    query = text(
        "SELECT Account.name AS name, Account.id AS id FROM Account"
        " WHERE Account.editor = %s" % ("true" if os.environ.get("HEROKU") else "1") + \
        " GROUP BY Account.name, Account.id"
    )
    return format_as_pair_id_name_and_alphabetize(db.engine.execute(query))

def getIssueOptions():
    query = text(
        "SELECT id, name FROM Issue"
    )
    return format_as_pair_id_name_and_alphabetize(db.engine.execute(query))

def getArticlesWithCondition(condition="(0 = 0)"):
    return getArticlesAmountCondition(condition=condition)

# Returns an array of [amount] articles where the condition [condition]
#  is satisfied
def getArticlesAmountCondition(amount=0, condition="(0=0)"):
    howmany = ""
    if amount > 0:
        howmany = " LIMIT %d" % int(amount)
    query = text(
        "SELECT Article.id AS id, Article.ready AS ready, Article.name AS name,"
        " Writer.name AS writer, Editor.name AS editor_in_charge FROM Article"
        " LEFT JOIN Account Writer ON Article.writer = Writer.id"
        " LEFT JOIN Account Editor ON Article.editor_in_charge = Editor.id"
        " WHERE %s" % condition +\
        " GROUP BY Article.id, Article.ready, Article.name, Writer.name, Editor.name" + howmany
    )
    return db.engine.execute(query)

def getArticleWithId(id):
    resultArray = getArticlesAmountCondition(amount=1, condition="Article.id = %d" % id)
    try:
        return resultArray.first()
    except:
        return None