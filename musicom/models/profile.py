from datetime import datetime
from ..db import mongo
from ..models.comment import Comment


class UserProfile(mongo.Document):
    # profile images
    img_url = mongo.StringField()
    min_img_url = mongo.StringField()

    # Personal information
    first_name = mongo.StringField(required=True)
    last_name = mongo.StringField(required=True)
    bio = mongo.StringField(max_length=512)
    status = mongo.StringField(max_length=24)
    region = mongo.StringField()

    # professional information
    youtube_link = mongo.StringField()
    principal_instrument = mongo.StringField()
    others_instruments = mongo.ListField(mongo.StringField())
    music_styles = mongo.ListField(mongo.StringField())

    comments = mongo.ListField(mongo.EmbeddedDocumentField(Comment))

    create_at = mongo.DateTimeField(default=datetime.utcnow)
    update_at = mongo.DateTimeField()
