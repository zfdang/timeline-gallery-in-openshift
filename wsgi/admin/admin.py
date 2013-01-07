# -*- coding: UTF-8 -*-
from flask import Blueprint, render_template, abort, url_for, session, current_app, flash, request
from database import init_db, db_session
from models import Photo, User
import os
from decorators import login_required

bp = Blueprint('admin', __name__)


@bp.route('/')
@login_required
def index():
    return render_template('admin/index.html')


@bp.route("/test")
def admin_test():
    users = User.query.filter(User.name == 'dang').all()
    for user in users:
        print user.id, user.name, user.password
        for photo in user.photos:
            print photo.id, photo.filename, photo.user_id, photo.user

    photos = Photo.query.all()
    for photo in photos:
        print photo.filename, photo.user_id, photo.user

    return "test"


@bp.route("/init")
def init():
    message = ""
    # clear login information in session
    session.pop('username', None)
    message += "session cleared!<br/>"
    # init database
    init_db()
    message += "database initialized!"
    # add init data for databases
    u1 = User(name='dang', email='zfang@freewheel.tv', password='zhengfa')
    db_session.add(u1)
    db_session.commit()

    p1 = Photo(filename="test1.jpg", saved_filename="saved_test1.jpg")
    p1.user_id = u1.id
    db_session.add(p1)

    p2 = Photo(filename="test2.jpg", saved_filename="saved_test2.jpg")
    p2.user_id = u1.id
    db_session.add(p2)

    p3 = Photo(filename="test3.jpg", saved_filename="saved_test3.jpg")
    db_session.add(p3)

    db_session.commit()

    # init upload folder
    if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
        os.mkdir(current_app.config['UPLOAD_FOLDER'])
        message += "upload folder created!"
    else:
        message += "upload folder existed!"
    flash(message)
    return render_template("admin/init.html")


@bp.route("/log/", defaults={'type': "error"})
@bp.route("/log/<type>/")
def show_log(type):
    if 'OPENSHIFT_APP_UUID' in os.environ:
        # access_log-20130102-000000-EST
        # error_log-20130102-000000-ES
        n = request.args.get("n", "100")
        folder = os.environ['OPENSHIFT_PYTHON_LOG_DIR']
        if type == "access":
            logfile = os.popen("ls -t %saccess_log* | head -n1" % folder).read()
        else:
            logfile = os.popen("ls -t %serror_log* | head -n1" % folder).read()
        logfile = logfile[:-1]
        contents = logfile + "<br><br>"
        contents += ("Number = %d" % (int(n))).center(80, "=")
        contents += "<br><br>"
        lines = os.popen("tail -n %d %s" % (int(n), logfile)).read()
        contents += "<br>".join(reversed(lines.split("\n")))
        return contents
    else:
        return "Not in OpenShift Environment"

