# -*- coding: UTF-8 -*-
from flask import Blueprint, render_template, url_for
from models import Photo, Setting
from timeline import Timeline
from sqlalchemy import desc
import datetime
from flaskext.babel import gettext as _

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
        start_date = setting.start_date.replace("-", ",")

    # convert timeline's start date to datetime obj
    album_start_date = datetime.datetime.strptime(start_date, "%Y,%m,%d")

    # collect all photos
    tl = Timeline(headline, text, start_date)
    photos = Photo.query.filter(Photo.visibility == True). all()
    for photo in photos:
        dt = photo.start_date.replace("-", ",")

        # convert photo's start date to datetime obj
        photo_start_date = datetime.datetime.strptime(dt, "%Y,%m,%d")
        days_in_album = (photo_start_date - album_start_date).days + 1
        # get No.D after timeline's start date
        asset_caption = _("Day %(value)d", value=days_in_album)

        text = photo.photo_text + "<BR/><BR/><A href='%s'><i class='icon-zoom-in'></i>%s</A>" % (url_for("photos.show_html", filename=photo.filename), photo.filename)

        tl.add_date(startDate=dt, headline=photo.headline, asset_media=url_for("photos.show_thumb", filename=photo.filename), text=text, asset_caption=asset_caption)
    return tl.get_json()
