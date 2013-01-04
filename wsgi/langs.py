# -*- coding: UTF-8 -*-
from flask import Blueprint, url_for, session, redirect, current_app
from flaskext.babel import refresh
from urllib import quote_plus, unquote_plus

# supported langs
SUPPORTED_LANGS = [
{'locale':'en', 'description':u'English'},
{'locale':'zh_CN', 'description':u'简体中文'},
]


bp = Blueprint('langs', __name__)


@bp.route("/list")
def list_lang():
    return str(SUPPORTED_LANGS)


# set lang for this session
@bp.route("/<lang_code>/", defaults={'url': None})
@bp.route("/<lang_code>/<url>")
def set_lang(lang_code, url):
    session['lang'] = lang_code
    refresh()
    if not url:
        url = quote_plus(url_for("index.index"))
    current_app.logger.info("set_lang: lang = %s, url = %s" % (session['lang'], unquote_plus(url)))
    return redirect(unquote_plus(url))
