import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from musicom.db import init_db
from flask_restful import Api
from musicom.api import init_routes
from musicom.errors import errors

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

api = Api(app, errors=errors)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

init_db(app)
init_routes(api)
