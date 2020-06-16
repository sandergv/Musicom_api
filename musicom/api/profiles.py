from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from ..models.profile import UserProfile
from datetime import datetime


class UserProfileListApi(Resource):

    @jwt_required
    def get(self):
        profile_id = request.args.get('profile_id')
        users = UserProfile.objects(id__ne=profile_id).only(
            'first_name',
            'last_name',
            'status',
            'principal_instrument',
            'min_img_url'
        )[:20]
        response = []
        for user in users:
            response.append({
                "id": str(user.id),
                "name": f"{user.first_name} {user.last_name}",
                "status": user.status,
                "principal_instrument": user.principal_instrument,
                "min_img_url": user.min_img_url
            })
        return {"users": response}, 200


class UserProfileApi(Resource):

    @jwt_required
    def get(self, profile_id):
        user = UserProfile.objects.only(
            'first_name',
            'last_name',
            'status',
            'principal_instrument',
            'min_img_url'
        ).get(id=profile_id)
        return {
            "id": str(user.id),
            "first_name": user.first_name,
            "last_name": user.last_name,
            "status": user.status,
            "principal_instrument": user.principal_instrument,
            "min_img_url": user.min_img_url
        }, 200


class ProfileApi(Resource):

    @jwt_required
    def get(self, profile_id):
        user = UserProfile.objects.get(id=profile_id)
        return self.to_json(user), 200

    # TODO
    @jwt_required
    def put(self, profile_id):
        body = request.get_json()
        user = UserProfile.objects.get(id=profile_id)
        user.update(**body)
        user.update_at = datetime.utcnow()
        user.save()
        return self.to_json(user), 200

    @staticmethod
    def to_json(user: UserProfile):
        return {
            "id": str(user.id),
            "name": user.first_name,
            "last_name": user.last_name,
            "status": user.status,
            "bio": user.bio,
            "image_url": user.img_url,
            "youtube_link": user.youtube_link,
            "principal_instrument": user.principal_instrument,
            "secondary_instrument": user.others_instruments,
            "music_styles": user.music_styles,
            "region": user.region,
            "comments": user.comments
        }


routes = [
    (UserProfileListApi, '/profiles'),
    (UserProfileApi, '/userProfile/<profile_id>'),
    (ProfileApi, '/profiles/<profile_id>'),
]
