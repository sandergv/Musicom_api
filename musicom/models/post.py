from datetime import datetime
from ..db import mongo
from .comment import Comment
from .embedded_profile import EmbeddedProfile


class Post(mongo.Document):
    title = mongo.StringField(required=True)
    content = mongo.StringField(required=True)
    post_type = mongo.StringField()
    comments = mongo.ListField(mongo.EmbeddedDocumentField(Comment))
    tags = mongo.ListField(mongo.StringField)
    user = mongo.EmbeddedDocumentField(EmbeddedProfile)
    create_at = mongo.DateTimeField(default=datetime.utcnow)
    update_at = mongo.DateTimeField()
