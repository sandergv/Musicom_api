from flask_bcrypt import generate_password_hash, check_password_hash
from datetime import datetime
from ..db import mongo


class User(mongo.Document):
    email = mongo.EmailField(required=True, unique=True)
    profile_id = mongo.StringField()
    password = mongo.StringField(required=True, min_length=8)
    created_at = mongo.DateTimeField(default=datetime.utcnow)
    update_at = mongo.DateTimeField()

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf-8')

    def check_password(self, password):
        return check_password_hash(self.password, password)


class UserConfig(mongo.Document):
    pass
