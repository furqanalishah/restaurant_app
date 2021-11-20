import os

from flask import url_for
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook

facebook_blueprint = make_facebook_blueprint(
    client_id=os.getenv('FACEBOOK_APP_ID'),
    client_secret=os.getenv('FACEBOOK_APP_SECRET'),
    redirect_to="google.redirect"
)


@facebook_blueprint.route("/facebook")
def index():
    if not facebook.authorized:
        return url_for("facebook.login")


@facebook_blueprint.route("/redirect")
def redirect():
    return "Facebook Authenticated"
