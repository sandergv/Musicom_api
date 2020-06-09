from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from ..models import post, profile
from ..models.embedded_profile import EmbeddedProfile
from ..models.comment import Comment, SubComment
from ..errors import (InternalServerError)

entities = {
    "profile": profile.UserProfile,
    "post": post.Post
}


class CommentApi(Resource):

    @jwt_required
    def post(self):
        body = request.get_json()
        comment_type = body['type']
        element_id = body['id']
        entity = entities[comment_type].objects.get(id=element_id)
        try:
            if comment_type == 'sub_comment':
                Comment.comments.append(
                    SubComment(
                        comment_by=EmbeddedProfile(**body['user']),
                        comment=body['comment'],
                    )
                )
            else:
                entity.comments.append(
                    Comment(
                        comment_by=EmbeddedProfile(**body['user']),
                        comment=body['comment'],
                    )
                )
        except Exception:
            raise InternalServerError

        return {}, 200

    def put(self):
        pass


routes = []
