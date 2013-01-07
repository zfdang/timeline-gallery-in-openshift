# -*- coding: UTF-8 -*-
from flask import Blueprint, render_template, abort, url_for, session, current_app, flash, request
from flask import send_from_directory
from database import init_db, db_session
from models import Photo, User
import os
from decorators import login_required
from pagination import Pagination
from uploads import get_saved_filename

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
@bp.route("/log/<type>")
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
        contents += lines.replace("\n", "<br>")
        return contents
    else:
        return "Not in OpenShift Environment"


@bp.route("/photos/", defaults={'page': 1})
@bp.route("/photos/page/<int:page>")
@login_required
def list_photos(page):
    file_per_page = current_app.config.get('FILE_PER_PAGE', 10)
    photos_count = Photo.query.count()
    photos = Photo.query.offset((page - 1) * file_per_page).limit(file_per_page)
    for photo in photos:
        photo.url = url_for(".show_photo", filename=photo.filename)

    pagination = Pagination(page, file_per_page, photos_count)
    return render_template("admin/photos.html", photos=photos, page=page, pagination=pagination)


@bp.route("/users")
@login_required
def list_users():
    users = User.query.all()
    return render_template("admin/users.html", users=users)


@bp.route('/photo/<filename>')
def show_photo(filename):
    saved_filename = get_saved_filename(filename)
    if not os.path.exists(os.path.join(current_app.config['UPLOAD_FOLDER'], saved_filename)):
        abort(404)
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], saved_filename, as_attachment=False)
