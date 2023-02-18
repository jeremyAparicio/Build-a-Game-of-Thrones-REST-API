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
from models import db, User
from models import Personajes
from models import Favoritos
from models import Continentes

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
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

    all_users = User.query.all()
    """
    new_users = []
    for i in range(len(all_users)):
        print(all_users[i])
        new_users.append(all_users[i].serialize())
    """
    all_users = list(map(lambda user: user.serialize() ,all_users))

    return jsonify(all_users), 200

@app.route("/personajes", methods=["GET"])
def get_all_perso():

    return jsonify({
        "mensaje": "Listado de los personajes"
    })

@app.route("/personajes/<int:id>", methods=["GET"])
def get_one_perso(id):

    return jsonify({
        "mensaje": "Información del personaje basandose en su id "+str(id)
    })

@app.route("/continentes", methods=["GET"])
def get_all_cont():

    return jsonify({
        "mensaje": "Listado de continentes"
    })

@app.route("/favoritos", methods=["GET"])
def get_all_fav():

    return jsonify({
        "mensaje": "Listado de items en favoritos"
    })

@app.route("/continentes/<int:id>", methods=["GET"])
def get_one_cont(id):

    return jsonify({
        "mensaje": "aca estara la info del continente con id "+str(id)
    })

@app.route("/favoritos/personajes/<int:personajes_id>", methods=['POST'])
def post_fav_perso(personajes_id):
    
    return jsonify({
        "mensaje": "el personaje con id "+ str(personajes_id) + " ha sido agregado"
    })

@app.route("/favoritos/personajes/<int:personajes_id>", methods=['DELETE'])
def delete_fav_perso(personajes_id):
    
    return jsonify({
        "mensaje": "el personaje con id "+ str(personajes_id) + " ha sido eliminado"
    })

@app.route("/favoritos/continentes/<int:continentes_id>", methods=['POST'])
def post_fav_cont(continentes_id):
    
    return jsonify({
        "mensaje": "el continente con id "+ str(continentes_id) + " ha sido agregado"
    })

@app.route("/favoritos/continentes/<int:continentes_id>", methods=['DELETE'])
def delete_fav_cont(continentes_id):
    
    return jsonify({
        "mensaje": "el continente con id "+ str(continentes_id) + " ha sido eliminado"
    })

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)