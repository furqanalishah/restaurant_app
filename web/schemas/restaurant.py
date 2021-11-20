from marshmallow import Schema
from marshmallow.fields import String, List
from marshmallow.validate import Length, Regexp


class _LocationQuerySchema(Schema):
    lat = String(
        required=True, allow_none=False,
        description="Latitude", example="34.206123"
    )
    long = String(
        required=True, allow_none=False,
        description="Longitude", example="72.029800"
    )


class AddRestaurantRequestSchema(Schema):
    name = String(
        required=True, allow_none=False,
        validate=Length(min=1, max=100),
        example="dam pukh",
        description="Name of the Restaurant."
    )
    email = String(
        required=True, allow_none=False,
        validate=[Regexp("[^@]+@[^@]+\.[^@]+")],
        example="name@somemail.com",
        description="Email Address of the User."
    )
    halal_foods = List(
        cls_or_instance=String(),
        required=True, allow_none=False
    )

    location_name = String(
        required=True, allow_none=False,
        validate=Length(min=1, max=100),
        description="Name of the Place."
    )

    latitude = String(
        required=True, allow_none=False,
        description="Latitude", example="34.206123"
    )
    longitude = String(
        required=True, allow_none=False,
        description="Longitude", example="72.029800"
    )


class RestaurantQuerySchema(Schema):
    name = String(
        validate=Length(min=1, max=100),
        description="Name of the Restaurant."
    )
    location_name = String(
        validate=Length(min=1, max=100),
        description="Name of the Place."
    )

    latitude = String(
        description="Latitude", example="34.206123"
    )
    longitude = String(
        description="Longitude", example="72.029800"
    )
