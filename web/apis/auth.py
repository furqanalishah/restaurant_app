import uuid

from apiflask import APIBlueprint, input, abort
from flask import url_for
from flask_mail import Message

from web import db, mail
from web.models import User
from web.schemas.auth import RegisterUserSchema, LoginUserSchema, ForgotPasswordSchema, NewPasswordSchema
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

    success_detail = {"status": "created", "detail": "Account is created."}
    return success_detail


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

    success_detail = {"status": "success", "detail": "You are now logged in."}
    return success_detail


@auth.post('/forgot_password')
@input(ForgotPasswordSchema)
def forgot_password(data):
    user = db.session.query(User).filter_by(email=data['email']).first()
    if not user:
        error_message = f"User with the email {data['email']} does not exist."
        abort(404, error_message)

    code = str(uuid.uuid4().hex)
    user.change_configuration = {"code": code}
    confirm_password_url = url_for('auth.confirm_code', code=code, username=user.username, _external=True)
    db.session.commit()

    msg = Message("Password Reset Request",
                  sender=user.email,
                  recipients=["mefurqan123@gmail.com"])

    msg.body = "Password Reset Request"
    msg.html = f"""You requested that the password for your Kennedy Family Recipes account be reset.
                    Please click the link below to reset your password:
                    
                    <p>
                    <a href="{confirm_password_url}">{confirm_password_url}</a>
                    </p>
                    
                    <p>
                    </p>"""
    mail.send(msg)

    success_detail = {"status": "success", "detail": "An email with code to reset password is on the way."}
    return success_detail


@auth.get('/confirm/<username>/<code>')
def confirm_code(username, code):
    user = db.session.query(User).filter_by(username=username).first()
    if not user:
        error_message = f"User with the username {username} does not exist."
        abort(404, error_message)

    if user.change_configuration.get("code") != code:
        error_message = "The code we sent you is not the same you have entered. Make sure they are the same."
        abort(404, error_message)

    success_message = {"status": "success", "detail": "Code is Confirmed"}
    return success_message


@auth.post('/password/new')
@input(NewPasswordSchema)
def create_new_password(data):
    user = db.session.query(User).filter_by(email=data["email"]).first()
    if not user:
        error_message = f"User with the email {data['email']} does not exist."
        abort(404, error_message)

    user.password_hash = Hash.bcrypt(data["new_password"])
    db.session.commit()

    success_message = {"status": "success", "detail": "You can now login with your new password."}
    return success_message
