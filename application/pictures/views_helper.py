from flask import redirect, render_template, request, url_for
from application.articles.models import Article
from application.pictures.models import Picture
from application.pictures.forms import replicate_picture_form, create_picture_form
from application import db

def update_picture_status(request, current_user):
    if not current_user.has_role("EDITOR"):
        return None
        
    form = request.form
    try:
        id = int(form["picture_id"])
    except:
        alert = {"type": "danger",
            "text": "Please don't try to hack me."}
        return alert

    picture = Picture.query.get(id)

    if not picture:
        alert = {"type": "danger",
                "text": "Something went wrong."}
    else:
        new_status = form["status"]
        try:
            if new_status is None:
                alert = {"type": "success",
                    "text": "Status updated!"}
                return alert
            new_status = int(new_status)
        except:
            alert = {"type": "danger",
                "text": "Please don't try to hack me."}
            return alert

        if 0 <= new_status and new_status <= 100:
            picture.status = new_status
            alert = {"type": "success",
                "text": "Status updated!"}
        else:
            alert = {"type": "danger",
                "text": "Please don't try to hack me."}
        db.session.commit()

    return alert

def delete_picture(request, current_user):
    if not current_user.has_role("ADMIN"):
        return None

    try:
        id = int(request.form["delete_picture"])
    except:
        alert = {"type": "danger",
            "text": "Please don't try to hack me."}
    
    picture_to_delete = Picture.query.get(id)
    if not picture_to_delete:
        alert = {"type": "danger",
            "text": "Somebody already deleted that picture."}
        return alert
    
    db.session.delete(picture_to_delete)
    db.session.commit()
    alert = {"type": "success",
        "text": "Picture deleted!"}
    return alert


def update_picture(picture, article, request):
    try:
        redirect_to = request.form["redirect_to"]
    except:
        redirect_to = url_for("articles_show", article_id = article.id)

    form = replicate_picture_form(request.form)

    if not form.validate():
        return render_template("pictures/new.html",
            updating_picture = True,
            redirect_to = redirect_to,
            picture = picture,
            article = article)
    
    picture.description = form.description.data
    picture.type =  form.type.data
    picture.responsible = form.responsible.data if form.responsible.data is not 0 else None
    db.session.commit()

    return redirect(redirect_to)


def show_prefilled_form(picture, article, request):
    redirect_to = request.referrer

    # create form
    form = create_picture_form()

    # preselect everything according to article's current status
    form.description.data = picture.description
    form.type.data = picture.type
    form.responsible.data = picture.responsible if picture.responsible is not None else 0

    return render_template("pictures/new.html",
        form = form,
        updating_picture=True,
        redirect_to=redirect_to,
        article=article,
        picture=picture)



    