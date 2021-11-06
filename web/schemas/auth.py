from marshmallow import Schema
from marshmallow.fields import String
from marshmallow.validate import Length, Regexp


class RegisterUserSchema(Schema):
    name = String(
        required=True, allow_none=False,
        validate=Length(min=5, max=50),
        example="name-1",
        description="Name of the User."

    )
    username = String(
        required=True, allow_none=False,
        validate=Length(min=5, max=50),
        example="name290",
        description="Username of the User."

    )
    email = String(
        required=True, allow_none=False,
        validate=[Regexp("[^@]+@[^@]+\.[^@]+")],
        example="name@somemail.com",
        description="Email Address of the User."

    )
    password = String(
        required=True, allow_none=False,
        validate=Length(min=8),
        example="password",
        description="Password of the User."
    )


class LoginUserSchema(Schema):
    email = String(
        required=True, allow_none=False,
        validate=[Regexp("[^@]+@[^@]+\.[^@]+")],
        example="name@somemail.com",
        description="Email Address of the User."

    )
    password = String(
        required=True, allow_none=False,
        validate=Length(min=8),
        example="password",
        description="Password of the User."
    )
