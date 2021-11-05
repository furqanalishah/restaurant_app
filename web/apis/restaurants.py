from apiflask import APIBlueprint

restaurants = APIBlueprint("restaurants", "restaurants", "Restaurants", url_prefix='/restaurants')


@restaurants.get("/")
def list_restaurants():
    return "list_restaurants"


@restaurants.get("/<restaurant_id>")
def get_restaurant(restaurant_id):
    return "get_restaurant"
