from flask import render_template, redirect, url_for
from application.articles.views_helper import update_status, delete_article
from application.pictures.views_helper import update_picture_status, delete_picture
from application.articles.models import Article
from application import db

# returns a dict that tells what to do next
def react_to_post_request(request, current_user):
    response = {"alert": None, "redirect": None, "open": 0}

    # if request is related to an artile, fetch the article
    if (request.form.get('update_status', None) or
        request.form.get('delete', None) or
        request.form.get('mark_ready', None) or
        request.form.get('grab', None)):

        try:
            id = int(request.form["article_id"])
        except:
            message = "Article related request did not contain parameter 'article_id'."
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
                response["redirect"] = redirect(url_for("error403"))
            response["alert"] = alert
            return response



        # request is to mark article's language checked
        elif request.form.get('mark_ready', None):
            if (not current_user.language_consultant and
                article.language_consultant == current_user.id):

                response["redirect"] = redirect(url_for("error403"))
                return response
            article.language_checked = True
            db.session.commit()
            alert = {"type": "success",
                "text": "Article '%s' marked 'language checked'" % article.name}
            response["alert"] = alert
            return response

        # request is to make current user article's language consultant
        elif request.form.get("grab", None):
            if not current_user.language_consultant:
                response["redirect"] = redirect(url_for("error403"))
                return response

            if article.language_consultant != None:
                alert = {"type": "danger",
                    "text": "Someone was faster than you!"}
                response["alert"] = alert
                return response
            elif article.editing_status < 100:
                alert = {"type": "danger",
                    "text": "Article's status has changed and" + \
                    " it is not ready for language checking."}
                response["alert"] = alert
                return response
            elif ((article.writer == current_user.id or
                article.editor_in_charge == current_user.id) and
                not current_user.admin):
                alert = {"type": "danger",
                    "text": "You are the editor or writer of this article."}
                response["alert"] = alert
                return response
            else:
                article.language_consultant = current_user.id
                db.session.commit()
                alert = {"type": "success",
                    "text": "Article '%s' is added to your task list!" % article.name }
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