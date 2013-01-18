# -*- coding: UTF-8 -*-
from flask import Blueprint, render_template, url_for, current_app, flash, request
from database import db_session
from models import User
from decorators import login_required
import json

bp = Blueprint('users', __name__)


@bp.route("/")
@login_required
def index():
    users = User.query.all()
    return render_template("admin/users.html", users=users)


@bp.route("/update/", methods=['POST'])
@login_required
def update():
    id = request.form['pk']
    name = request.form['name']
    value = request.form['value']
    current_app.logger.info("user.update: id=%s, name=%s, value=%s" % (id, name, value))

    # find user record firsr
    user = User.query.get(id)
    if not user:
        return "invalid user"

    # update field by name
    if name == "username":
        user.name = value
        db_session.add(user)
        db_session.commit()
        return value
    elif name == "email":
        user.email = value
        db_session.add(user)
        db_session.commit()
        return value
    elif name == "password":
        user.set_password(value)
        db_session.add(user)
        db_session.commit()
        return value
    elif name == "delete":
            username = user.name
            db_session.delete(user)
            db_session.commit()
            result = {
                'status': 'success',
                'message': '%s has been deleted!' % (username)
            }
            return json.dumps(result)

    return "invalid action"
