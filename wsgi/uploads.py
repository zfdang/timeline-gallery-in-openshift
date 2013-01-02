import os
from flask import request, redirect, url_for, current_app
from flask import Blueprint, render_template
from urllib import quote
from werkzeug import secure_filename
from flask import send_from_directory

from database import db_session, init_db
from models import Photo
from flaskext.babel import gettext as _
from pagination import Pagination

uploads = Blueprint('uploads', __name__)


# find upload data path
if 'OPENSHIFT_APP_UUID' in os.environ:
    UPLOAD_FOLDER = os.path.join(os.environ['OPENSHIFT_DATA_DIR'], "uploads")
else:
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "..", "data", "uploads")
# allowed extensions for uploading
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


# check file extensions
def allowed_file(filename):
    filename = filename.lower()
    return '.' in filename and \
       filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@uploads.route("/init")
def init():
    message = ""
    init_db()
    message += "database initialized!<BR/>"
    if not os.path.exists(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)
        message += "upload folder created!<BR/>"
    return message


@uploads.route("/", defaults={'page': 1})
@uploads.route("/page/<int:page>")
def list_file(page):
    file_per_page = current_app.config.get('FILE_PER_PAGE', 10)
    photos_count = Photo.query.count()
    photos = Photo.query.offset((page - 1) * file_per_page).limit(file_per_page)
    for photo in photos:
        photo.url = url_for(".show_file", filename=photo.saved_filename)

    pagination = Pagination(page, 5, photos_count)
    return render_template("uploads/list.html", photos=photos, upload_link=url_for(".upload_file"), page=page, pagination=pagination)


@uploads.route('/file/<filename>')
def show_file(filename):
    _filename = secure_filename(quote(filename.encode("UTF-8")))
    current_app.logger.info("filename original=%s, decoded=%s" % (filename, _filename))
    return send_from_directory(UPLOAD_FOLDER, _filename, as_attachment=False)


@uploads.route('/upload', methods=['GET', 'POST'])
def upload_file():
    current_app.logger.info("upload_folder = %s", UPLOAD_FOLDER)
    if request.method == "GET":
        return render_template('uploads/uploads.html', action_url=url_for(".upload_file"))
    elif request.method == "POST":
        # current_app.logger.info("upload_file: POST")
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(quote(file.filename.encode("UTF-8")))
            current_app.logger.info("filename original = %s, escaped = %s" % (file.filename, filename))
            file.save(os.path.join(UPLOAD_FOLDER, filename))

            photo = Photo(filename=file.filename, saved_filename=filename)
            db_session.add(photo)
            db_session.commit()

            return redirect(url_for(".list_file"))
        current_app.logger.info("Invalid file extension: %s" % (file.filename))
        return redirect(url_for(".list_file"))
