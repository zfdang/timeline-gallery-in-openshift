from flask import Blueprint, render_template, url_for, request, session, redirect, flash, current_app
from urllib import unquote_plus
from models import User


bp = Blueprint('login', __name__)


@bp.route('/', methods=['GET', 'POST'], defaults={'next': None})
@bp.route('/url/<next>', methods=['GET', 'POST'])
def authentication(next):
    class Failed(Exception):
        def __init__(self, results):
            super(Failed, self).__init__()
            self.results = results

    current_app.logger.info("next = %s" % (next))
    if request.method == 'GET':
        if not next:
            next = url_for('admin.index')
        return render_template('admin/login.html', next=next)
    else:
        try:
            username = request.form['username']
            password = request.form['password']
            next = request.form['next']
            current_app.logger.info("attempt to login: name=%s, ip=%s" % (username,  request.remote_addr))
            users = User.query.filter(User.name == username).all()
            if len(users) != 1:
                raise Failed("invalid username")
            user = users[0]
            if not user.check_password(password):
                raise Failed("Invalid password")
            session['username'] = user.name
            session['user_id'] = user.id
            flash("You have logined successfully!")
            return redirect(unquote_plus(next))
        except Failed as f:
            current_app.logger.info(f.results)
            flash("Invalid username/password!")
            return render_template('admin/login.html', next=next)
