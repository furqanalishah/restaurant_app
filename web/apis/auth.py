from apiflask import APIBlueprint, input, abort

from web import db
from web.models import User
from web.schemas.auth import RegisterUserSchema, LoginUserSchema
from web.session import get_db_session
from web.utils import Hash

auth = APIBlueprint("auth", "authentication", "Authentication")


@auth.post("/register")
@input(RegisterUserSchema)
def register(data):
    user = db.session.query(User).filter_by(email=data['email']).first()
    if user:
        error_message = f"User with the email {data['email']} already exist."
        abort(404, error_message)

    new_user = User(**data)
    try:
        with get_db_session() as db_session:
            db_session.add(new_user)
            db_session.commit()
    except Exception as e:
        print(e)

    success_message = {"message": "created"}
    return success_message


@auth.post("/login")
@input(LoginUserSchema)
def login(data):
    user = db.session.query(User).filter_by(email=data['email']).first()
    if not user:
        error_message = f"No user is registered with email {data['email']}."
        abort(404, error_message)

    if not Hash.verify(user.password_hash, data["password"]):
        error_message = f"username or password is incorrect."
        abort(401, error_message)

    success_message = {"message": "success"}
    return success_message


@auth.get('/forgot_password')
def forgot_password():
    return 'Forgot Password'
