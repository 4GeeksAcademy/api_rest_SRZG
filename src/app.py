"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Favorite_Types, Favorites, Planets, Vehicles, People
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


@app.route('/planets', methods=["GET"])
def handle_get_planets():
    planets = Planets.query.all()
    planets = list(map(lambda p: p.serialize(), planets))

    return jsonify(planets)


@app.route('/vehicles', methods=["GET"])
def handle_get_vehicles():
    vehicles = Vehicles.query.all()
    vehicles = list(map(lambda v: v.serialize(), vehicles))

    return jsonify(vehicles)


@app.route('/people', methods=["GET"])
def handle_get_people():
    people = People.query.all()
    people = list(map(lambda p: p.serialize(), people))

    return jsonify(people)


@app.route('/favorite/<item_type>/<int:item_id>', methods=["POST"])
def handle_post_favorite(item_type, item_id):
    new_favorite = Favorites()
    if item_type == "people":
        new_favorite.type = Favorite_Types.people
        new_favorite.people_id = item_id
        new_favorite.user_id = 1

    elif item_type == "planets":
        new_favorite.type = Favorite_Types.planets
        new_favorite.planet_id = item_id
        new_favorite.user_id = 1

    elif item_type == "vehicles":
        new_favorite.type = Favorite_Types.vehicles
        new_favorite.vehicle_id = item_id
        new_favorite.user_id = 1

    else:
        return jsonify({"msg": "Wrong favorite type"}), 404
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"msg": "Creates succesfully", "favorite": new_favorite.serialize()}), 201


@app.route('/favorites/<int:userId>', methods=["GET"])
def handle_get_favorites(userId):
    user_favorites = Favorites.query.filter_by(user_id=userId).all()
    user_favorites = list(map(lambda fav: fav.serialize(), user_favorites))
    return jsonify(user_favorites), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
