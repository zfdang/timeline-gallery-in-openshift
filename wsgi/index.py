from flask import Blueprint, render_template, abort, url_for, jsonify, current_app
from jinja2 import TemplateNotFound
from models import Photo
from timeline import Timeline


index = Blueprint('index', __name__)


@index.route('/')
def show():
    try:
        return render_template('index.html', username='zfdang', age="32")
    except TemplateNotFound:
        abort(404)


@index.route("timeline")
def timeline_json():
    tl = Timeline("Chinese PRC", "this is the text", '2011,9,30')

    photos = Photo.query.all()
    for photo in photos:
        tl.add_date('2011,10,1', photo.filename, url_for("uploads.show_file", filename=photo.filename))
    return tl.get_json()


if __name__ == "__main__":
    import os
    print os.path.dirname(__file__)
