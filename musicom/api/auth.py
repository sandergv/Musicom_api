import datetime

from flask import Response, request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from ..models.user import User
from ..models.profile import UserProfile
from mongoengine.errors import (
    NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError
)
from ..errors import (
    InternalServerError, SchemaValidationError, EmailAlreadyExistsError,
    UsernameAlreadyExistsError, UnauthorizedError
)


class SignupApi(Resource):

    def post(self):
        body = request.get_json()
        try:
            user = User(
                email=body['email'],
                password=body['password']
            )
            user.hash_password()
            user.save()
            user_profile = UserProfile(
                first_name=body['first_name'],
                last_name=body['last_name']
            )
            user_profile.save()
            user.profile_id = str(user_profile.id)
            user.save()
            expires = datetime.timedelta(days=365)
            access_token = create_access_token(identity=str(user.id), expires_delta=expires)
            return {
                'id': str(user.id),
                'profile_id': user.profile_id,
                'token': access_token
            }, 200

        except ValidationError:
            raise SchemaValidationError
        except NotUniqueError:
            raise EmailAlreadyExistsError


class LoginApi(Resource):

    def post(self):
        body = request.get_json()
        user = None
        try:
            user = User.objects.get(email=body['email'])
            profile = UserProfile.objects.only('first_name', 'last_name').get(id=user.profile_id)
        except DoesNotExist:
            raise UnauthorizedError

        auth = user.check_password(body['password'])
        if not auth:
            raise UnauthorizedError

        expires = datetime.timedelta(days=365)
        access_token = create_access_token(identity=str(user.id), expires_delta=expires)
        return {
            'id': str(user.id),
            'profile_id': user.profile_id,
            'first_name': profile.first_name,
            'last_name': profile.last_name,
            'token': access_token
        }, 200


class ChangePasswordApi(Resource):

    @jwt_required
    def post(self):
        body = request.get_json()
        user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)
        auth = user.check_password(body['password'])
        if not auth:
            raise UnauthorizedError

        user.password = body['new_password']
        user.hash_password()
        user.update()  # check

        return {"success": True}, 200


routes = [
    (SignupApi, '/auth/signup'),
    (LoginApi, '/auth/login'),
    (ChangePasswordApi, '/auth/changePass')
]
