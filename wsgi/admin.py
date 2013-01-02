from flask import Blueprint, render_template, abort, redirect, url_for
from jinja2 import TemplateNotFound
from database import init_db, db_session
from models import User


admin = Blueprint('admins', __name__)


@admin.route('/')
def admin_show():
    try:
        return render_template('admin/admin.html')
    except TemplateNotFound:
        abort(404)


@admin.route("/init")
def admin_init_db():
    init_db()
    return "database initialized!"


@admin.route("/add")
def admin_add_user():
    import random
    chars = [chr(x) for x in range(ord('a'), ord('z'))]
    random.shuffle(chars)
    name = "".join(chars[0:random.randint(0, len(chars))])
    email = "".join(chars[0:random.randint(0, len(chars))]) + "@freewheel.tv"
    u = User(name=name, email=email)
    db_session.add(u)
    db_session.commit()

    return redirect(url_for(".admin_list_user"))


@admin.route("/list")
def admin_list_user():
    users = User.query.all()
    return render_template("admin/users.html", users=users)
