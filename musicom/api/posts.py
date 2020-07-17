from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from ..models.post import Post
from ..models.embedded_profile import EmbeddedProfile


class PostApi(Resource):

    @jwt_required
    def get(self, post_id):
        post = Post.objects.get(id=post_id)
        return {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "user": post.user,
            "create_at": post.create_at,
            "tags": post.tags,
            "comments": post.comments
        }

    @jwt_required
    def post(self, post_id):
        body = request.get_json()
        post = Post(
            title=body["title"],
            content=body["content"],
            comments=body["comments"],
            tags=body["tags"],
            user=EmbeddedProfile(
                profile_id=body["user"]["profile_id"],
                name=body["user"]["name"],
                min_img_url=body["user"]["img_url"]
            )
        )
        post.save()
        return {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "user": post.user,
            "create_at": post.create_at,
            "tags": post.tags,
            "comments": post.comments
        }

    def put(self, post_id):
        pass


class PostsListApi(Resource):
    pass


routes = [
    (PostApi, "/post/<post_id>"),
    (PostsListApi, "/posts")
]
