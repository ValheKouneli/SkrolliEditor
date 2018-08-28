from flask import redirect, render_template, request, url_for
from application.pictures.models import Picture
from application import db

def update_picture_status(request, current_user, id):
    if not current_user.editor:
        return None
        
    form = request.form
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