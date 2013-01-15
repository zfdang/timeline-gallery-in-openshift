# -*- coding: UTF-8 -*-
from flask import Blueprint, render_template, url_for
from models import Photo, Setting
from timeline import Timeline
from sqlalchemy import desc

bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    headline = "Timeline Photo Headline"
    host = "127.0.0.1"
    # find settings
    settings = Setting.query.order_by(desc(Setting.id)).all()
    if len(settings) > 0:
        setting = settings[0]
        headline = setting.headline
        host = setting.host

    return render_template('index.html', title=headline, host=host)


@bp.route("timeline")
def timeline_json():
    headline = "Timeline Photo Headline"
    text = "this is the text"
    start_date = '2012,4,12'

    # find settings
    settings = Setting.query.order_by(desc(Setting.id)).all()
    if len(settings) > 0:
        setting = settings[0]
        headline = setting.headline
        text = setting.setting_text
        start_date = setting.start_date

    # collect all photos
    tl = Timeline(headline, text, start_date)
    photos = Photo.query.all()
    for photo in photos:
        dt = photo.start_date.replace("-", ",")
        tl.add_date(dt, photo.filename, url_for("photos.show_photo", filename=photo.filename))
    return tl.get_json()
