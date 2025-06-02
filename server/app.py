#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request,session
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)

@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

class RestaurantResource(Resource):
    def get(self, id=None):
        if id is not None:
            restaurant = db.session.get(Restaurant, id)
            if not restaurant:
                return {"error": "Restaurant not found"}, 404
            return restaurant.to_dict(), 200

        restaurants = Restaurant.query.all()
        return [
            restaurant.to_dict(only=("id", "name", "address"))
            for restaurant in restaurants
        ], 200


    
    def delete(self, id):
        restaurant = db.session.get(Restaurant, id)
        if not restaurant:
            return {"error": "Restaurant not found"}, 404

        db.session.delete(restaurant)
        db.session.commit()
        return {}, 204



class PizzaList(Resource):
     def get(self):
        pizzas = Pizza.query.all()
        return [
            pizza.to_dict(only=("id", "name", "ingredients"))
            for pizza in pizzas
        ], 200
class RestaurantPizzaList(Resource):
    def post(self):
        data = request.get_json()
        try:
            new_restaurant_pizza = RestaurantPizza(
                price=data["price"],
                pizza_id=data["pizza_id"],
                restaurant_id=data["restaurant_id"]
            )
            db.session.add(new_restaurant_pizza)
            db.session.commit()
            return new_restaurant_pizza.to_dict(), 201
        
        except Exception :
            return {"errors": ["validation errors"]}, 400

# api.add_resource(RestaurantList, '/restaurants')
api.add_resource(RestaurantResource,'/restaurants' ,'/restaurants/<int:id>')
api.add_resource(PizzaList, '/pizzas')
api.add_resource(RestaurantPizzaList, '/restaurant_pizzas')

if __name__ == "__main__":
    app.run(port=5555, debug=True)