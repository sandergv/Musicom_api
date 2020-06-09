from ..db import mongo


class EmbeddedProfile(mongo.EmbeddedDocument):
    name = mongo.StringField()
    profile_id = mongo.StringField()
    min_img_url = mongo.StringField()
