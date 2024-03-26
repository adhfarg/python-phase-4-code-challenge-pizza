#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
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

@app.get('/restaurants')
def get_restaurants():
    restaurants = Restaurant.query.all()
    return [r.to_dict(rules=['-restaurant_pizzas']) for r in restaurants], 200

@app.get('/restaurants/<int:id>')
def get_restaurant_by_id(id):
    restaurant = db.session.get(Restaurant, id)
    if not restaurant:
        return {'error': "Restaurant not found"}, 404
    return restaurant.to_dict(), 200

@app.delete('/restaurants/<int:id>')
def delete_restaurant(id):
    restaurant = db.session.get(Restaurant, id)
    if not restaurant:
        return {'error': "Restaurant not found"}, 404
    
    db.session.delete(restaurant)
    db.session.commit()
    return {}, 204

@app.get('/pizzas')
def get_pizzas():
    pizzas = Pizza.query.all()
    return [p.to_dict(rules=['-restaurant_pizzas']) for p in pizzas], 200

@app.post('/restaurant_pizzas')
def post_restaurant_pizza():
    data = request.json
    try:
        rp = RestaurantPizza(price=data.get('price'), restaurant_id=data.get('restaurant_id'), pizza_id=data.get('pizza_id'))
        db.session.add(rp)
        db.session.commit()
        return rp.to_dict(), 201
    except Exception as e:
        print(e)
        return {'errors':["validation errors"]}, 400
    
if __name__ == "__main__":
    app.run(port=5555, debug=True)
