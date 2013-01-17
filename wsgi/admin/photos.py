# -*- coding: UTF-8 -*-
from flask import Blueprint, render_template, abort, url_for, current_app, request
from flask import send_from_directory
from models import Photo
from database import db_session
import os
from decorators import login_required
from pagination import Pagination
from uploads import get_saved_filename, get_noexif_filename, get_thumb_filename
from exiv2 import get_image_exif, get_image_date
import json

bp = Blueprint('photos', __name__)


@bp.route("/", defaults={'page': 1})
@bp.route("/page/<int:page>")
@login_required
def index(page):
    file_per_page = current_app.config.get('FILE_PER_PAGE', 10)
    photos_count = Photo.query.count()
    photos = Photo.query.order_by(Photo.filename).offset((page - 1) * file_per_page).limit(file_per_page)
    for photo in photos:
        photo.url = url_for(".show_photo", filename=photo.filename)

    pagination = Pagination(page, file_per_page, photos_count)
    return render_template("admin/photos.html", photos=photos, page=page, pagination=pagination)


@bp.route('/update/', methods=['POST'])
@login_required
def update():
    if request.method == "POST":
        target = request.form['name']
        id = request.form['pk']
        value = request.form['value']
        current_app.logger.info("photo_edit: id=%s, target=%s, value=%s" % (id, target, value))

        # find photo instance first
        photo = Photo.query.get(id)
        if not photo:
            return "invalid id"

        if target == "start_date":
            photo.start_date = value
            db_session.add(photo)
            db_session.commit()
            return photo.start_date
        elif target == "headline":
            photo.headline = value
            db_session.add(photo)
            db_session.commit()
            return photo.headline
        elif target == "text":
            photo.photo_text = value
            db_session.add(photo)
            db_session.commit()
            return photo.photo_text
        elif target == "visibility":
            if value == "True":
                photo.visibility = True
            else:
                photo.visibility = False
            db_session.add(photo)
            db_session.commit()
            return value
        elif target == "delete":
            filename = photo.filename
            db_session.delete(photo)
            db_session.commit()
            result = {
                'status': 'success',
                'message': '%s has been deleted!' % (filename)
            }
            return json.dumps(result)

    return "Unknown action"


@bp.route('/html/<filename>')
def show_html(filename):
    noexif_filename = get_noexif_filename(filename)
    current_app.logger.info("serve html file: %s" % (noexif_filename))
    if not os.path.exists(os.path.join(current_app.config['UPLOAD_FOLDER'], noexif_filename)):
        abort(404)
    photo_url = url_for(".show_photo", filename=filename)
    photo_thumb_url = url_for(".show_thumb", filename=filename)
    photo_name = filename
    return render_template("photo.html", photo_url=photo_url, photo_thumb_url=photo_thumb_url, photo_name=photo_name)


@bp.route('/file/<filename>')
def show_photo(filename):
    # noexif_filename = get_saved_filename(filename)
    noexif_filename = get_noexif_filename(filename)
    current_app.logger.info("serve noexif file: %s" % (noexif_filename))
    if not os.path.exists(os.path.join(current_app.config['UPLOAD_FOLDER'], noexif_filename)):
        abort(404)
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], noexif_filename, as_attachment=False)


@bp.route('/thumb/<filename>')
def show_thumb(filename):
    thumb_filename = get_thumb_filename(filename)
    current_app.logger.info("serve thumb file: %s" % (thumb_filename))
    if not os.path.exists(os.path.join(current_app.config['UPLOAD_FOLDER'], thumb_filename)):
        abort(404)
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], thumb_filename, as_attachment=False)


@bp.route('/exif/<filename>')
def show_photo_exif(filename):
    saved_filename = get_saved_filename(filename)
    exif_info = get_image_exif(saved_filename=saved_filename, filepath=current_app.config['UPLOAD_FOLDER'])
    return exif_info
