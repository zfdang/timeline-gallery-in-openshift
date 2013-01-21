# -*- coding: UTF-8 -*-
from flask import Blueprint, render_template, request
from database import db_session
from models import Monitor
from sqlalchemy import desc

bp = Blueprint('monitor', __name__)


@bp.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        monitors = Monitor.query.order_by(desc(Monitor.id)).limit(50)
        return render_template("admin/monitor.html", monitors=monitors)
    elif request.method == 'POST':
        ipv4 = request.form['ipv4']
        monitor = Monitor(ipv4)
        db_session.add(monitor)
        db_session.commit()
        return "OK"
