from application.articles.views_helper import delete_article, update_status
from flask import redirect, url_for, render_template
from application.articles.models import Article

def react_to_post_request(request, current_user):
    
    response = {"redirect": None, "alert": {}, "open": 0}

    # featch article that is the target of the request
    try:
        id = int(request.form["article_id"])
    except:
        message = "Request to update article status or delete article did not contain parameter 'article_id'."
        response["redirect"] = render_template("error500.html", message=message)
        return response
    
    article = Article.query.get(id)
    if not article:
        response["redirect"] = redirect(url_for("error404"))
        return response

    response["open"] = id



    # request is to update article status
    if request.form.get('update_status', None):
        # returns None if user is not authorized
        alert = update_status(request, article, current_user)
        if not alert:
            response["return"] = redirect(url_for("error403"))
            return response
        response["alert"] = alert
        return response



    # request is to delete article
    elif request.form.get('delete', None):
        # returns None if user is not authorized
        alert = delete_article(request, article, current_user)
        if not alert:
            response
            response["redirect"] = redirect(url_for("error403"))
            return response
        response["alert"] = alert
        return response


    # request did not match any given type
    return response