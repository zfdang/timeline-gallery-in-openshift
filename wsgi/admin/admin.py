# -*- coding: UTF-8 -*-
from flask import Blueprint, render_template, session, current_app, flash, request
from database import init_db, db_session
from models import User
import os
from decorators import login_required


bp = Blueprint('admin', __name__)


@bp.route('/')
@login_required
def index():
    return render_template('admin/index.html')


@bp.route('/init')
def init():
    messages = []

    # clear login information in session
    session.pop('username', None)
    messages.append("session cleared!")

    # init database
    init_db()  # this operation won't create tables if they exist

    # add init data for databases
    users = User.query.filter(User.name == "admin").all()
    if len(users) == 0:
        u1 = User(name='admin', email='admin@youremail.com', password='Password2012')
        db_session.add(u1)
        db_session.commit()
        messages.append("user 'admin' added!")
    else:
        messages.append("user 'admin' exists!")

    # init upload folder
    if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
        os.mkdir(current_app.config['UPLOAD_FOLDER'])
        messages.append("upload folder created!")
    else:
        messages.append("upload folder existed!")

    for message in messages:
        flash(message)

    return render_template('admin/init.html')


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
