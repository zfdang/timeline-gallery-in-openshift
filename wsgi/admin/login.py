from flask import Blueprint, render_template, url_for, request, session, redirect, flash, current_app
from urllib import unquote_plus


bp = Blueprint('login', __name__)


@bp.route('/', methods=['GET', 'POST'], defaults={'next': None})
@bp.route('/url/<next>', methods=['GET', 'POST'])
def authentication(next):
    current_app.logger.info("next = %s" % (next))
    if request.method == 'GET':
        if not next:
            next = url_for('admin.index')
        return render_template('admin/login.html', next=next)
    else:
        username = request.form['username']
        password = request.form['password']
        next = request.form['next']
        if username == 'dang' and password == 'zhengfa':
            session['username'] = username
            flash("You have logined successfully!")
            return redirect(unquote_plus(next))
        else:
            flash("Invalid username/password!")
            return render_template('admin/login.html', next=next)
