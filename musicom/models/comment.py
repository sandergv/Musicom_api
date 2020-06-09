from datetime import datetime
from ..db import mongo
from .embedded_profile import EmbeddedProfile


class SubComment(mongo.EmbeddedDocument):
    comment = mongo.StringField(required=True)
    comment_by = mongo.EmbeddedDocumentField(EmbeddedProfile)
    create_at = mongo.DateTimeField(default=datetime.utcnow)
    update_at = mongo.DateTimeField()


class Comment(mongo.EmbeddedDocument):
    comment = mongo.StringField(required=True)
    comment_by = mongo.EmbeddedDocumentField(EmbeddedProfile)
    create_at = mongo.DateTimeField(default=datetime.utcnow)
    update_at = mongo.DateTimeField()

    comments = mongo.ListField(mongo.EmbeddedDocumentField(SubComment))
