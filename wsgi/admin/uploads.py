import os
from flask import request, redirect, url_for, current_app, flash
from flask import Blueprint, render_template
from urllib import quote
from werkzeug import secure_filename

from database import db_session
from models import Photo

bp = Blueprint('uploads', __name__)
ALLOWED_EXTENSIONS = set(['bmp', 'tiff', 'png', 'jpg', 'jpeg', 'gif'])


# check file extensions
def allowed_file(filename):
    # allowed extensions for uploading
    # check file extensions
    filename = filename.lower()
    return '.' in filename and \
       filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def get_saved_filename(filename):
    if filename:
        return secure_filename(quote(filename.encode("UTF-8")))
    return None


@bp.route('/', methods=['GET', 'POST'])
def upload_file():
    current_app.logger.info("upload folder = %s", current_app.config['UPLOAD_FOLDER'])
    if request.method == "GET":
        return render_template('admin/uploads.html', action_url=url_for(".upload_file"))
    elif request.method == "POST":
        # current_app.logger.info("upload_file: POST")
        file = request.files['file']
        if file and allowed_file(file.filename):
            saved_filename = get_saved_filename(file.filename)
            current_app.logger.info("filename original = %s, escaped = %s" % (file.filename, saved_filename))
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], saved_filename))

            photo = Photo(filename=file.filename, saved_filename=saved_filename)
            db_session.add(photo)
            db_session.commit()

            flash("File: %s uploaded successfully" % (file.filename))
            return redirect(url_for("admin.list_photos"))
        else:
            current_app.logger.info("Invalid file extension: %s" % (file.filename))
            flash("Invalid file extension: %s" % (file.filename))
            return redirect(url_for(".upload_file"))
