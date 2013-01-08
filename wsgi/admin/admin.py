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
    messages = []

    # clear login information in session
    session.pop('username', None)
    messages.append("session cleared!")

    # init database
    init_db()
    messages.append("database initialized!")
    # add init data for databases
    user = User.query.filter(User.name == "dang").all()
    if not user:
        u1 = User(name='dang', email='zfang@freewheel.tv', password='zhengfa')
        db_session.add(u1)
        db_session.commit()
        messages.append("user 'dang' added!")
    else:
        messages.append("user 'dang' exists!")

    # init upload folder
    if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
        os.mkdir(current_app.config['UPLOAD_FOLDER'])
        messages.append("upload folder created!")
    else:
        messages.append("upload folder existed!")

    for message in messages:
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
