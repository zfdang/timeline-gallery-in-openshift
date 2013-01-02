from flask import Flask, request, url_for, render_template
import pages
import admin
import index
import uploads
from database import db_session
from flaskext.babel import Babel

app = Flask(__name__)
app.config.from_object('settings.DevelopmentConfig')
babel = Babel(app)  # use BABEL_DEFAULT_LOCALE from app.config

# register all blueprints
app.register_blueprint(index.index, url_prefix='/')
app.register_blueprint(pages.pages, url_prefix='/pages')
app.register_blueprint(admin.admin, url_prefix='/admin')
app.register_blueprint(uploads.uploads, url_prefix='/uploads')


# pagination helper method
def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)
app.jinja_env.globals['url_for_other_page'] = url_for_other_page


# To use SQLAlchemy in a declarative way with your app, you just have to put the following code into your app module. Flask will automatically remove database sessions at the end of the request for you:
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    print app.url_map
    app.run()
