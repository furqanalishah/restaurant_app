import os

from flask import url_for
from flask_dance.contrib.google import make_google_blueprint, google

google_blueprint = make_google_blueprint(
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    redirect_to="google.redirect"
)


@google_blueprint.route("/google")
def index():
    if not google.authorized:
        return url_for("google.login")
        # return redirect(url_for("google.login"))
    resp = google.get("/plus/v1/people/me")
    assert resp.ok, resp.text
    return "You are {email} on Google".format(email=resp.json()["emails"][0]["value"])


@google_blueprint.route("/redirect")
def redirect():
    return "Google Authenticated"
