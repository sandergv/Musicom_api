from datetime import datetime
from ..db import mongo
from .comment import Comment
from .embedded_profile import EmbeddedProfile


class Post(mongo.Document):
    posted_by = mongo.StringField(required=True)
    title = mongo.StringField(required=True)
    content = mongo.StringField(required=True)
    post_type = mongo.StringField(required=True)
    comments = mongo.ListField(mongo.EmbeddedDocumentField(Comment))
    user = mongo.EmbeddedDocumentField(EmbeddedProfile)
    create_at = mongo.DateTimeField(default=datetime.utcnow)
    update_at = mongo.DateTimeField()
