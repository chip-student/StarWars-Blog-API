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
from models import db, User, Character, Planet, Favplanet, Favcharacter
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

    # Favplanet, Favcharacter
    personaje_query = db.Query(Favplanet, Favcharacter).join()

    # map the results and your list of people  inside of the all_people variable
    all_personajes = list(map(lambda x: x.serialize(), personaje_query))

    return jsonify(all_personajes), 200
    

@app.route('/all_personajes', methods=['GET'])
def get_all_personaje():

    # get all the people
    personaje_query = Personaje.query.all()

    # map the results and your list of people  inside of the all_people variable
    all_personajes = list(map(lambda x: x.serialize(), personaje_query))

    return jsonify(all_personajes), 200

@app.route('/personajes/<int:id>', methods=['GET'])
def get_personaje_id(id):

    # get only the ones id
    personaje_query = Personaje.query.filter_by(id=id)

    # map the results and your list of people  inside of the all_people variable
    all_personajes = list(map(lambda x: x.serialize(), personaje_query))

    return jsonify(all_personajes), 200

@app.route('/all_planetas', methods=['GET'])
def get_all_planetas():

    # get all the people
    planeta_query = Planeta.query.all()

    # map the results and your list of people  inside of the all_people variable
    all_planetas = list(map(lambda x: x.serialize(), planeta_query))

    return jsonify(all_planetas), 200

@app.route('/planetas/<int:id>', methods=['GET'])
def get_planeta_id(id):

    # get only the ones id
    planeta_query = Planeta.query.filter_by(id=id)

    # map the results and your list of people  inside of the all_people variable
    all_planetas = list(map(lambda x: x.serialize(), planeta_query))

    return jsonify(all_planetas), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)