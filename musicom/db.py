from flask_mongoengine import MongoEngine

import os

mongo = MongoEngine()


def init_db(app):
    uri = os.getenv('MONGO_URI')
    if os.getenv('PROJECT_ENV') == 'dev':
        user = os.getenv('MONGO_USER')
        password = os.getenv('MONGO_PASS')
        db = os.getenv('MONGO_DATABASE')
        host = os.getenv('MONGO_HOSTNAME')
        uri = f"mongodb://{user}:{password}@{host}:27017/{db}?authSource=admin"

    app.config['MONGODB_SETTINGS'] = {'host': uri}
    mongo.init_app(app)
