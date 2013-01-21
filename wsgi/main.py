# -*- coding: UTF-8 -*-
from flask import Flask, request, url_for, render_template, session, redirect
from urllib import quote_plus, unquote_plus

# app starts here
app = Flask(__name__)
app.config.from_object('settings.DevelopmentConfig')


# database module depends on app.config['DATABASE_URL']
from database import initialize
initialize(app.config['DATABASE_URL'])


# To use SQLAlchemy in a declarative way with your app, you just have to put the following code into your app module. Flask will automatically remove database sessions at the end of the request for you:
@app.teardown_request
def shutdown_session(exception=None):
    from database import db_session
    db_session.remove()


# register all blueprints
import index
import langs
from admin import admin, uploads, login, photos, users, settings, monitor
app.register_blueprint(index.bp, url_prefix='/')
app.register_blueprint(langs.bp, url_prefix='/lang')
app.register_blueprint(admin.bp, url_prefix='/admin')
app.register_blueprint(photos.bp, url_prefix='/admin/photos')
app.register_blueprint(users.bp, url_prefix='/admin/users')
app.register_blueprint(settings.bp, url_prefix='/admin/settings')
app.register_blueprint(uploads.bp, url_prefix='/admin/uploads')
app.register_blueprint(login.bp, url_prefix='/admin/login')
app.register_blueprint(monitor.bp, url_prefix='/admin/monitor')


@app.route("/favicon.ico")
def favicon():
    return redirect(url_for('static', filename='favicon.ico'))


# babel related settings
from flaskext.babel import Babel
babel = Babel(app)  # use BABEL_DEFAULT_LOCALE from app.config


@babel.localeselector
def get_locale():
    # if a user is logged in, use the locale from the user settings
    if 'lang' in session:
        user_lang = session['lang']
    else:
        # otherwise try to guess the language from the user accept
        # header the browser transmits.
        user_lang = request.accept_languages.best_match(['zh_CN', 'en'])
    # app.logger.info("get_locale: lang = %s" % (user_lang))
    return user_lang


@babel.timezoneselector
def get_timezone():
    user_tz = None
    if 'timezone' in session:
        user_tz = session['timezone']
    return user_tz


# generate variables for all context
@app.context_processor
def inject_langs():
    return dict(langs=langs.SUPPORTED_LANGS)


@app.context_processor
def inject_scheme_host_headline():
    from models import Setting
    from sqlalchemy import desc
    headline = "Timeline Photo Headline"
    host = request.host
    scheme = request.scheme
    # find settings
    try:
        settings = Setting.query.order_by(desc(Setting.id)).all()
        if len(settings) > 0:
            setting = settings[0]
            if setting.headline:
                headline = setting.headline
            if setting.host:
                host = setting.host
    except:
        pass
    return {'headline': headline, 'host': host, 'scheme': scheme}


# pagination helper method
# two required components: pagination.py & pagination.html
def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)
app.jinja_env.globals['url_for_other_page'] = url_for_other_page


# jinja2 filters to quote_plus urls
@app.template_filter('quoteplus')
def quoteplus_filter(s):
    # url_for(endpoint, **values)
    # all values will be url_encode again. so we have to unqote the url, then quote it again.
    return quote_plus(unquote_plus(s))


@app.template_filter("bjtime")
def convert_to_bjtime_filter(s):
    from datetime import datetime
    from pytz import timezone
    import pytz
    utctime = datetime(s.year, s.month, s.day, s.hour, s.minute, s.second, s.microsecond, tzinfo=pytz.utc)
    cstinfo = timezone('Asia/Shanghai')
    ltime = utctime.astimezone(cstinfo)
    fmt = '%Y-%m-%d %H:%M:%S %Z%z'
    ltime_str = ltime.strftime(fmt)
    return ltime_str


# error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    print app.url_map
    app.run()
