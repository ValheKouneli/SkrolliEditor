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

def getIssueOptions():
    query = text(
        "SELECT id, name FROM Issue"
    )
    issues = db.engine.execute(query)
    formatted = [(0, None)]
    for issue in issues:
        formatted.append((issue.id, issue.name))
    return formatted

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
        " GROUP BY Article.id" + howmany
    )
    return db.engine.execute(query)

def getArticleWithId(id):
    resultArray = getArticlesAmountCondition(amount=1, condition="Article.id = %d" % id)
    try:
        return resultArray.first()
    except:
        return None