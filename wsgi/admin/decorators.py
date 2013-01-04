from functools import wraps
from flask import request, redirect, url_for, session, current_app
from urllib import quote_plus


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not 'username' in session:
            current_app.logger.info("quoted url = %s" % (quote_plus(request.url)))
            current_app.logger.info("redirected url = %s" % (url_for('login.authentication', next=quote_plus(request.url))))
            return redirect(url_for('login.authentication', next=quote_plus(request.url)))
        return f(*args, **kwargs)
    return decorated_function
