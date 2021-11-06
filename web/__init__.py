from apiflask import APIFlask
from flask_sqlalchemy import SQLAlchemy

from config import flask_config
from web.apis.facebook import facebook_blueprint
from web.apis.google import google_blueprint
from web.apis.oauth import o_auth

db = SQLAlchemy()


def create_app():
    app = APIFlask(__name__, title="Halal Restaurants Application", version="1.0")
    config = flask_config['development']
    app.config.from_object(config)
    app.logger.setLevel(config.LOGGING_LEVEL_MAPPED)
    db.init_app(app)
    db.app = app

    from web.apis.auth import auth
    from web.apis.restaurants import restaurants
    app.register_blueprint(auth)
    app.register_blueprint(o_auth, url_pefix="/oauth")
    app.register_blueprint(google_blueprint, url_pefix="/google")
    app.register_blueprint(facebook_blueprint, url_pefix="/facebook")
    app.register_blueprint(restaurants, url_prefix="/restaurants")

    return app
