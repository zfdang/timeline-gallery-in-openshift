# -*- coding: UTF-8 -*-
from flask import Blueprint, render_template, url_for, current_app, flash, request
from database import db_session
from models import User
from decorators import login_required

bp = Blueprint('users', __name__)


@bp.route("/")
@login_required
def index():
    users = User.query.all()
    return render_template("admin/users.html", users=users)
