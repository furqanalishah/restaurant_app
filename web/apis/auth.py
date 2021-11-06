from flask import redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from apiflask import APIBlueprint, APIFlask, Schema, input
from apiflask.fields import Integer, String
from apiflask.validators import Length, OneOf

from web import db
from web.models.users import User

auth = APIBlueprint("auth", "authentication", "Authentication", url_prefix='/auth')


class UserSchema(Schema):
    id = String()
    name = String(required=True, validate=Length(0, 100))
    username = String(required=True, validate=Length(0, 100))
    email = String(required=True, validate=Length(0, 100))
    password = String(required=True, validate=Length(0, 100))


@auth.post('/signup')
@input(UserSchema)
def signup(data):
    name = request.json['name']
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    user = User.query.filter_by(
        username=username).first()  # if this returns a user, then the email already exists in database

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(name=name, email=email, username=username,
                    password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.get("/login")
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))  # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    return redirect(url_for('main.profile'))


@auth.get('/forgot_password')
def forgot_password():
    return 'Forgot Password'


@auth.get('/logout')
# @login_required
def logout():
    # logout_user()
    return redirect(url_for('main.index'))
