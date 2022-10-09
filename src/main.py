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
from models import db, User, Characters, Planets, Favorites_Characters, Favorites_Planets
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

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)


@app.route('/users', methods=['GET'])
def get_user():
    allUser = User.query.all()
    allUser = list(map(lambda elemento: elemento.serialize(), allUser))

    return jsonify(allUser), 200

@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user_id = request.args.get('user_id')
    user = User.query.get(user_id)

    favorites  = user.favorites_characters
    favorites.extend(user.favorites_planets)

    favorites = list(map(lambda elemento: elemento.serialize(), favorites))

    return jsonify(favorites), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST', 'DELETE'])
def add_favorite_planet(planet_id):
    user_id = request.args.get('user_id')
    user = User.query.get(user_id)

    if request.method == 'DELETE':
        for favorite_planet in user.favorites_planets:
            if favorite_planet.planets_id == planet_id:
                favorite_planet.delete()
                return 'ok', 200

    planet = Planets.query.get(planet_id)

    new_favorite = Favorites_Planets(
        user_id = user.id,
        planets_id = planet.id
    )

    new_favorite.save()

    return 'ok', 200

@app.route('/favorite/character/<int:character_id>', methods=['POST', 'DELETE'])
def add_favorite_character(character_id):
    user_id = request.args.get('user_id')
    user = User.query.get(user_id)


    if request.method == 'DELETE':
        for favorite_character in user.favorites_characters:
            if favorite_character.characters_id == character_id:
                favorite_character.delete()
                
                return 'ok', 200


    character = Characters.query.get(character_id)

    new_favorite = Favorites_Characters(
        user_id = user.id,
        characters_id = character.id
    )

    new_favorite.save()

    return 'ok', 200



# Listar todos los registros de people en la base de datos
@app.route('/characters', methods=['GET'])
def get_characters():
    allCharacters = Characters.query.all()
    allCharacters = list(map(lambda elemento: elemento.serialize(), allCharacters))

    return jsonify(allCharacters), 200

# Listar la información de una sola people
@app.route('/characters/<int:characters_id>', methods=['GET'])
def get_one_character(characters_id):
    one_character = Characters.query.get(characters_id)
    print(one_character)
    if one_character is None:
        return 'not found', 404

    return jsonify(one_character.serialize()), 200

# Listar los registros de planets en la base de datos
@app.route('/planets', methods=['GET'])
def get_planets():
    allPlanets = Planets.query.all()
    allPlanets = list(map(lambda elemento: elemento.serialize(), allPlanets))

    return jsonify(allPlanets), 200

# Listar la información de un solo planet
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_one_planet(id):
    one_planet = Planets.query.get(id)
    if one_planet is None:
        return 'not found', 404

    return jsonify(planet.serialize()), 200



# Adicionalmente necesitamos crear los siguientes endpoints para que podamos tener usuarios en nuestro blog:

# [GET] /users Listar todos los usuarios del blog
# [GET] /users/favorites Listar todos los favoritos que pertenecen al usuario actual.
# [POST] /favorite/planet/<int:planet_id> Añade un nuevo planet favorito al usuario actual con el planet id = planet_id.
# [POST] /favorite/people/<int:planet_id> Añade una nueva people favorita al usuario actual con el people.id = people_id.
# [DELETE] /favorite/planet/<int:planet_id> Elimina un planet favorito con el id = planet_id`.
# [DELETE] /favorite/people/<int:people_id> Elimina una people favorita con el id = people_id.