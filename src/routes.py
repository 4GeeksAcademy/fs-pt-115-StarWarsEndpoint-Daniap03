from flask import Flask, request, jsonify, Blueprint
from models import db, User, Character, Vehicles, Planets

api = Blueprint("api", __name__)


@api.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    print(users)
    return jsonify([user.serialize() for user in users]), 200


@api.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg":"User not found"}), 404
    return jsonify(user.serialize()), 200

@api.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data.get("username") or not data.get("firstname") or not data.get("lastname") or not data.get("email") or not data.get("password"):
        return jsonify({"msg":"All fields are required"}), 400
    
    new_user = User(
        username=data["username"],
        firstname=data["firstname"],
        lastname=data["lastname"],
        email=data["email"],
        password=data["password"]
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.serialize()), 200

@api.route("/characters", methods=["GET"])
def get_characters():
    characters = Character.query.all()
    return jsonify([character.serialize() for character in characters]), 200


@api.route("/characters/<int:character_id>", methods=["GET"])
def get_character(character_id):
    characters = Character.query.get(character_id)
    if not characters:
        return jsonify({"msg":"Character not found"}), 404
    return jsonify(characters.serialize()), 200


@api.route("/characters", methods=["POST"])
def create_character():
    data = request.get_json()
    if not data.get("name"):
        return jsonify ({"msg": "The field is required"}), 400
    
    new_character = Character(
        name=data["name"]
    )

    db.session.add(new_character)
    db.session.commit()

    return jsonify(new_character.serialize()), 200



@api.route("/planets", methods=["GET"])
def get_planets():
    planetas = Planets.query.all()
    return jsonify([planets.serialize() for planets in planetas]), 200


@api.route("/planets/<int:planets_id>", methods=["GET"])
def get_planet(planets_id):
    planet = Planets.query.get(planets_id)
    if not planet:
        return jsonify({"msg":"Planet not found"}), 404
    return jsonify(planet.serialize()), 200


@api.route("/planets", methods=["POST"])
def create_planet():
    data = request.get_json()
    if not data.get("name"):
        return jsonify ({"msg": "The field is required"}), 400
    
    new_planet = Planets(
        name=data["name"]
    )

    db.session.add(new_planet)
    db.session.commit()

    return jsonify(new_planet.serialize()), 200


@api.route("/vehicles", methods=["GET"])
def get_vehicles():
    vehiculos = Vehicles.query.all()
    return jsonify([vehicles.serialize() for vehicles in vehiculos]), 200


@api.route("/vehicles/<int:vehicles_id>", methods=["GET"])
def get_vehicle(vehicles_id):
    vehiculo = Vehicles.query.get(vehicles_id)
    if not vehiculo:
        return jsonify({"msg":"Vehicle not found"}), 404
    return jsonify(vehiculo.serialize()), 200


@api.route("/vehicles", methods=["POST"])
def create_vehicles():
    data = request.get_json()
    if not data.get("name"):
        return jsonify ({"msg": "The field is required"}), 400
    
    new_vehicle = Vehicles(
        name=data["name"]
    )

    db.session.add(new_vehicle)
    db.session.commit()

    return jsonify(new_vehicle.serialize()), 200


@api.route("/<int:user_id>/favorite_char/<int:character_id>", methods=["POST"])
def add_favorite_character(user_id, character_id):
    user = db.session.get(User, user_id)
    character = db.session.get(Character, character_id)

    if not user or not character:
        return jsonify({"msg": "user or character not found"}), 404
    
    if character in user.favorite_characters:
        return jsonify({"msg": "character already in favorites"}), 400
    
    user.favorite_characters.append(character)

    db.session.commit()

    return jsonify(user.serialize()),200


@api.route("/<int:user_id>/favorite_vehicle/<int:vehicle_id>", methods=["POST"])
def add_favorite_vehicle(user_id, vehicle_id):
    user = db.session.get(User, user_id)
    vehicle = db.session.get(Vehicles, vehicle_id)

    if not user or not vehicle:
        return jsonify({"msg": "user or vehicle not found"}), 404
    
    if vehicle in user.favorite_vehicles:
        return jsonify({"msg": "vehicle already in favorites"}), 400
    
    user.favorite_vehicles.append(vehicle)

    db.session.commit()

    return jsonify(user.serialize()),200
        

@api.route("/<int:user_id>/favorite_planet/<int:planet_id>", methods=["POST"])
def add_favorite_planet(user_id, planet_id):
    user = db.session.get(User, user_id)
    planet = db.session.get(Planets, planet_id)

    if not user or not planet:
        return jsonify({"msg": "user or planet not found"}), 404
    
    if planet in user.favorite_planets:
        return jsonify({"msg": "planet already in favorites"}), 400
    
    user.favorite_planets.append(planet)

    db.session.commit()

    return jsonify(user.serialize()),200   


@api.route("/<int:user_id>/favorite_char/<int:character_id>", methods=["DELETE"])
def remove_favorite_character(user_id, character_id):
    user = db.session.get(User, user_id)
    character = db.session.get(Character, character_id)

    if not user or not character:
        return jsonify({"msg": "user or character not found"}), 404
    
    if character in user.favorite_characters:
        user.favorite_characters.remove(character)
        db.session.commit()

    return jsonify(user.serialize()),200


@api.route("/<int:user_id>/favorite_vehicle/<int:vehicle_id>", methods=["DELETE"])
def remove_favorite_vehicle(user_id, vehicle_id):
    user = db.session.get(User, user_id)
    vehicle = db.session.get(Vehicles, vehicle_id)

    if not user or not vehicle:
        return jsonify({"msg": "user or vehicle not found"}), 404
    
    if vehicle in user.favorite_vehicles:
        user.favorite_vehicles.remove(vehicle)
        db.session.commit()
    
    return jsonify(user.serialize()),200


@api.route("/<int:user_id>/favorite_planet/<int:planet_id>", methods=["DELETE"])
def remove_favorite_planet(user_id, planet_id):
    user = db.session.get(User, user_id)
    planet = db.session.get(Planets, planet_id)

    if not user or not planet:
        return jsonify({"msg": "user or planet not found"}), 404
    
    if planet in user.favorite_planets:
        user.favorite_planets.remove(planet)
        db.session.commit()
    
    return jsonify(user.serialize()),200