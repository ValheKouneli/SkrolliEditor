from application import db, os
from sqlalchemy.sql import text
from wtforms import ValidationError
import re

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

# DANGER DANGER, never call this without verifying that condition is not shady
def getArticlesWithCondition(condition="(0 = 0)"):
    return getArticlesAmountCondition(condition=condition)

# Returns an array of [amount] articles where the condition [condition]
#  is satisfied.
# DANGER DANGER, never call this without verifying that condition is not shady
def getArticlesAmountCondition(amount=0, condition="(0=0)"):
    howmany = ""
    order = ""
    if amount > 0:
        howmany = " LIMIT %d" % int(amount)
    elif amount == 0:
        howmany = ""
    if amount != 1:
        order = " ORDER BY Issue.name"
    query = text(
        "SELECT"
        " Article.id AS id,"
        " Issue.name AS issue,"
        " Synopsis.content AS synopsis,"
        " Article.writing_status AS writing_status,"
        " Article.editing_status AS editing_status,"
        " Article.ready AS ready,"
        " Article.name AS name,"
        " Article.writer AS writer_id,"
        " Article.editor_in_charge AS editor_id,"
        " Writer.name AS writer,"
        " Editor.name AS editor_in_charge,"
        " LanguageConsultant.name AS language_consultant"
        " FROM Article"
        " LEFT JOIN Account Writer ON Article.writer = Writer.id"
        " LEFT JOIN Account Editor ON Article.editor_in_charge = Editor.id"
        " LEFT JOIN Account LanguageConsultant ON Article.language_consultant = LanguageConsultant.id"
        " LEFT JOIN Issue ON Article.issue = Issue.id"
        " LEFT JOIN Synopsis ON Synopsis.article_id = Article.id"
        " WHERE %s" % condition +\
        " GROUP BY Article.id, Issue.name, Article.ready, Synopsis.content, Article.name, Article.writer, Writer.name, Editor.name, LanguageConsultant.name" + \
        howmany + order
    )
    return db.engine.execute(query)

def getArticleWithId(id):
    if not isinstance(id, int):
        return None

    resultArray = getArticlesAmountCondition(amount=1, condition="Article.id = %d" % id)
    try:
        return resultArray.first()
    except:
        return None

def getPicturesForArticle(id):
    if not isinstance(id, int):
        return None
    condition = "Picture.article_id = %d" % id
    return getPicturesWithCondition(condition=condition)

def getPictureWithId(id):
    if not isinstance(id, int):
        return None
    resultArray = getPicturesAmountCondition(amount=1, condition="Picture.id = %d" % id)
    return resultArray.first()

def getPicturesWithCondition(condition="0=0"):
    return getPicturesAmountCondition(condition=condition)

# DANGER DANGER never call this function without
# making sure that the condition is safe
def getPicturesAmountCondition(amount=0, condition="0=0"):
    howmany = ""
    order = ""
    if amount > 0:
        howmany = " LIMIT %d" % int(amount)
    if amount != 1:
        order = " ORDER BY Article.name"
    query = text(
        "SELECT Picture.id AS id,"
        " Picture.type AS type,"
        " Picture.article_id AS article_id,"
        " Picture.description AS description,"
        " Article.name AS article,"
        " Article.id AS article_id,"
        " Responsible.name AS responsible,"
        " Picture.status AS status"
        " FROM Picture"
        " LEFT JOIN Account Responsible ON Picture.responsible = Responsible.id"
        " LEFT JOIN Article Article ON Picture.article_id = Article.id"
        " WHERE %s" % condition + \
        " GROUP BY Picture.id, Picture.type, Picture.article_id, Picture.description, Article.name,"
        " Article.id, Responsible.name, Picture.status" +
        howmany + order
    )
    return db.engine.execute(query)
    

def name_only_contains_certain_characters(form, field):
    message = 'Name contains illegal characters or does not start with a capital letter.'

    pattern = re.compile(r"^[A-ZÀÈÌÒÙÁÉÍÓÚÝÂÊÎÔÛÃÑÕÄËÏÖÜŸÇßØÅåÆ]" + \
        r"[a-zA-ZàèìòùÀÈÌÒÙáéíóúýÁÉÍÓÚÝâêîôûÂÊÎÔÛãñõÃÑÕäëïöüÿÄËÏÖÜŸçÇßØøÅåÆæœ\'\- ]*$")
    if not pattern.match(field.data):
        raise ValidationError(message)
    return

# form validator,
# sets a flag "bigger_input_field" to the field
def needs_a_bigger_input_field():
    def _needs_a_bigger_input_field(form, field):
        pass
    _needs_a_bigger_input_field.field_flags = ('bigger_input_field', )
    return _needs_a_bigger_input_field
        