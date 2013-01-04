# -*- coding: UTF-8 -*-
from flask import Blueprint, render_template, url_for
from models import Photo
from timeline import Timeline


bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    return render_template('index.html', username='zfdang', age="32")


@bp.route("timeline")
def timeline_json():
    tl = Timeline("Chinese PRC", "this is the text", '2011,9,30')

    photos = Photo.query.all()
    for photo in photos:
        tl.add_date('2011,10,1', photo.filename, url_for("admin.show_photo", filename=photo.filename))
    return tl.get_json()
