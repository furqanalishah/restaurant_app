from pprint import pprint

from apiflask import APIBlueprint, input, abort
from flask import jsonify

from web import db
from web.models import Restaurant
from web.schemas.restaurant import AddRestaurantRequestSchema, RestaurantQuerySchema
from web.session import get_db_session

restaurants = APIBlueprint("restaurants", "restaurants", "Restaurants", url_prefix='/restaurants')


@restaurants.get("/")
@input(RestaurantQuerySchema, location='query')
def list_restaurants(filter_params):
    if not filter_params:
        restaurants_list = [restaurant.to_json() for restaurant in db.session.query(Restaurant).all()]
        return jsonify(restaurants_list)
    restaurants_list = [
        restaurant.to_json()
        for restaurant in
        db.session.query(Restaurant).filter_by(**filter_params).all()
    ]
    return jsonify(restaurants_list)


@restaurants.get("/<restaurant_id>")
def get_restaurant(restaurant_id):
    restaurant = db.session.query(Restaurant).get(restaurant_id)
    if not restaurant:
        error_message = f"Restaurant with the id {restaurant_id} does not exist."
        abort(404, error_message)

    return restaurant.to_json()


@restaurants.post("/")
@input(AddRestaurantRequestSchema)
def add_restaurant(data):
    pprint(data)
    with get_db_session() as db_session:
        new_restaurant = Restaurant(**data)
        db_session.add(new_restaurant)
        db_session.commit()

    success_detail = {"status": "created", "detail": "New Restaurant is Added."}
    return success_detail
