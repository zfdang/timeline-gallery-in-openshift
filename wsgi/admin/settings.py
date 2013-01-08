# -*- coding: UTF-8 -*-
from flask import Blueprint, render_template, url_for, current_app, flash, request, redirect
from database import db_session
from models import Setting
from decorators import login_required
from sqlalchemy import desc
from flaskext.babel import gettext as _

bp = Blueprint('settings', __name__)


@bp.route("/", methods=['GET', 'POST'])
@login_required
def index():
    if request.method == "GET":
        # find the latest setting record
        settings = Setting.query.order_by(desc(Setting.id)).all()
        if len(settings) > 0:
            setting = settings[0]
        else:
            setting = None
        return render_template("admin/settings.html", setting=setting)
    elif request.method == "POST":
        # get post data
        setting_id = request.form['setting_id']
        host = request.form['host']
        headline = request.form['headline']
        setting_text = request.form['text']
        start_date = request.form['start_date']
        current_app.logger.info("%s, %s, %s, %s, %s" % (setting_id, host, headline, setting_text, start_date))

        # find or create setting object
        setting = None
        if setting_id:
            setting = Setting.query.get(int(setting_id))
        if not setting:
            setting = Setting()

        # udpate db
        setting.host = host
        setting.headline = headline
        setting.setting_text = setting_text
        setting.start_date = start_date
        db_session.add(setting)
        db_session.commit()
        flash(_("Setting updated!"))
        return redirect(url_for(".index"))
