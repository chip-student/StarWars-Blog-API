"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, json
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets, Favorites

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
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
def get_all_user():

    # get all the people
    user_query = User.query.all()

    # map the results and your list of people  inside of the all_people variable
    all_user = list(map(lambda x: x.serialize(), user_query))

    return jsonify(all_user), 200

# [GET] /users/<int:user_id>/FavoritessGet all the Favoritess that belong to the user with the id = user_id.
@app.route('/getuserfav/<int:id>', methods=['GET'])
def get_user_fav(id):

    # get only the ones id
    Favorites_query = Favorites.query.filter_by(iduser=id)

    Favorites_query = list(map(lambda x: x.serialize(), Favorites_query))

    return jsonify(Favorites_query), 200
# [POST] /users/<int:user_id>/FavoritessAdd a new Favorites to the user with the id = user_id

@app.route('/postuserfav/<int:id>', methods=['POST'])
def add_fav(id):

    request_body=request.get_json()
    fav = Person(idpeople=request_body["idpeople"], iduser=id, idplanet=request_body["idplanet"])
    db.session.add(fav)
    db.session.commit()

    return jsonify("El favorito se agrego de manera satisfactoria"), 200

# [DELETE] /favorite/<int:favorite_id>Delete favorite with the id = favorite_id
@app.route('/deleteuserfav/<int:favorite_id>', methods=['DELETE'])
def delete_fav(id):

    # get only the ones named "Joe"
    favorite_query = Favorites.query.filter_by(id=favorite_id)

    if favorite_query is None:
        raise APIException('User not found', status_code=404)
        db.session.delete(favorite_query)
        db.session.commit()

    return jsonify("El favorito se elimino de manera satisfactoria"), 200

@app.route('/people', methods=['GET'])
def get_all_people():

    # get all the people
    people_query = People.query.all()

    # map the results and your list of people  inside of the all_people variable
    all_people = list(map(lambda x: x.serialize(), people_query))

    return jsonify(all_people), 200

@app.route('/people/<int:id>', methods=['GET'])
def get_people_id(id):

    # get only the ones id
    people_query = People.query.filter_by(id=id)

    # map the results and your list of people  inside of the all_people variable
    all_people = list(map(lambda x: x.serialize(), people_query))

    return jsonify(all_people), 200

@app.route('/planets', methods=['GET'])
def get_all_planets():

    # get all the planet
    planet_query = Planets.query.all()

    # map the results and your list of planet  inside of the all_planet variable
    all_planets = list(map(lambda x: x.serialize(), planet_query))

    return jsonify(all_planets), 200

@app.route('/planets/<int:id>', methods=['GET'])
def get_planet_id(id):

    # get only the ones id
    planet_query = Planets.query.filter_by(id=id)

    # map the results and your list of people  inside of the all_people variable
    all_planets = list(map(lambda x: x.serialize(), planet_query))

    return jsonify(all_planets), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
