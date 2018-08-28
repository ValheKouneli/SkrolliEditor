from flask import render_template, redirect, url_for
from application.articles.views_helper import update_status, delete_article
from application.pictures.views_helper import update_picture_status, delete_picture
from application.articles.models import Article

# returns a dict that tells what to do next
def react_to_post_request(request, current_user):
    response = {"alert": None, "redirect": None, "open": 0}

    # if request is related to an artile, fetch the article
    if (request.form.get('update_status', None) or
        request.form.get('delete', None)):

        try:
            id = int(request.form["article_id"])
        except:
            message = "Article status update or delete request did not contain parameter 'article_id'."
            response["redirect"] = render_template("error500.html", message=message)
            return response

        article = Article.query.get(id)
        if not article:
            response["redirect"] = redirect(url_for("error404"))
            return response


        # request is to update article status
        if request.form.get('update_status', None):
            # returns None if user is not authorized
            alert = update_status(request, article, current_user)
            if not alert:
                response["redirect"] = redirect(url_for("error403"))
            try:
                response["open"] = request.form["article_id"]
            except:
                response["open"] = 0
            response["alert"] = alert
            return response


        # request is to delete article
        elif request.form.get('delete', None):
            alert = delete_article(request, article, current_user)
            if not alert:
                return redirect(url_for("error403"))
            response["alert"] = alert
            return response


    # request is to delete picture
    elif request.form.get('delete_picture', None):
        # returns None if user is not authorized
        alert = delete_picture(request, current_user)
        if not alert:
            return redirect(url_for("error403"))
        response["alert"] = alert
        return response


    # request is to update picture status
    elif request.form.get('update_picture_status', None):
        # returns None if user is not authorized
        alert = update_picture_status(request, current_user)
        if not alert:
            return redirect(url_for("error403"))
        response["alert"] = alert
        try:
            response["open"] = request.form["picture_id"]
        except:
            response["open"] = 0
        return response

    # request does not match any known options
    return response