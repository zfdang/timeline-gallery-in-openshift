from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

pages = Blueprint('pages', __name__)


@pages.route('/', defaults={'page': 'index'})
@pages.route('/page/<int:page>')
def pages_show(page):
    try:
        return render_template('pages/pages.html')
    except TemplateNotFound:
        abort(404)
