from apiflask import APIBlueprint

o_auth = APIBlueprint("oauth", "authentication", "Authentication")


@o_auth.post("/google/login")
def oauth_google_login(data):
    return "oauth_google_login"


@o_auth.post("/facebook/login")
def oauth_facebook_login(data):
    return "oauth_facebook_login"
