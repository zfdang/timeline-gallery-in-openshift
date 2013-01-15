# -*- coding: UTF-8 -*-
import os
from flask import request, url_for, current_app, session
from flask import Blueprint, render_template
from urllib import quote
from werkzeug import secure_filename
import json

from database import db_session
from models import Photo
from decorators import login_required

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


def dump(obj):
    for attr in dir(obj):
        print "obj.%s = %s" % (attr, getattr(obj, attr))


def get_file_size(file):
    file.seek(0, 2)  # Seek to the end of the file
    size = file.tell()  # Get the position of EOF
    file.seek(0)  # Reset the file position to the beginning
    return size


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    current_app.logger.info("upload_file, method = %s, folder=%s", request.method, current_app.config['UPLOAD_FOLDER'])
    if request.method == "GET":
        return render_template('admin/uploads.html')
    elif request.method == "POST":
        #generating json response array
        result = []
        for inputname, fileobj in request.files.items():
            # filename = fileobj.filename
            # current_app.logger.info("filename = %s" % (filename))
            # dump(fileobj)
            # fileobj = request.files[filename]
            # current_app.logger.info("filename = %s, file size = %d" % (filename, get_file_size(fileobj.file)))
            if fileobj and allowed_file(fileobj.filename):
                if Photo.query.filter(Photo.filename == fileobj.filename).count() > 0:
                    result.append({"name": fileobj.filename,
                                   "size": 0,
                                   "error": "Duplicated filename",
                                   "url": "",
                                   "thumbnail_url": "",
                                   "delete_url": "",
                                   "delete_type": "POST"})
                    continue
                saved_filename = get_saved_filename(fileobj.filename)
                filesize = get_file_size(fileobj.stream)
                current_app.logger.info("filename original = %s, escaped = %s, size = %d" % (fileobj.filename, saved_filename, filesize))
                fileobj.save(os.path.join(current_app.config['UPLOAD_FOLDER'], saved_filename))

                photo = Photo(filename=fileobj.filename, saved_filename=saved_filename)
                photo.size = filesize
                photo.user_id = session['user_id']
                db_session.add(photo)
                db_session.commit()

                result.append({"name": fileobj.filename,
                               "size": filesize,
                               "url": url_for("photos.show_photo", filename=fileobj.filename),
                               "thumbnail_url": url_for("photos.show_photo", filename=fileobj.filename),
                               "delete_url": "",
                               "delete_type": "POST"})
            else:
                current_app.logger.info("Invalid file extension: %s" % (fileobj.filename))
                result.append({"name": fileobj.filename,
                               "error": "Invalid file extension",
                               "size": "",
                               "url": "",
                               "thumbnail_url": "",
                               "delete_url": "",
                               "delete_type": "POST"})

        # https://github.com/blueimp/jQuery-File-Upload/wiki/Setup
        # response formats
        final_result = {}
        final_result['files'] = result
        response_data = json.dumps(final_result)
        current_app.logger.info("response = %s" % (response_data))
        return response_data
