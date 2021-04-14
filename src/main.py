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
from models import db, User, People, Planets, Favorite
#from models import Person

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

# [GET] /users/<int:user_id>/favoritesGet all the favorites that belong to the user with the id = user_id.
@app.route('/userfav/<int:id>', methods=['GET'])
def get_user_fav(id):

    # get only the ones id
    favorite_query = Favorite.query.filter_by(iduser=id)
    # join_query = db.session.query(Favorite, People).join(People).filter(Favorite.iduser == id).all()

    favorite_query = list(map(lambda x: x.serialize(), favorite_query))

    return jsonify(favorite_query), 200
    

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
