from apiflask import APIBlueprint

auth = APIBlueprint("auth", "authentication", "Authentication", url_prefix='/auth')


@auth.get("/login")
def login():
    return "Login"
