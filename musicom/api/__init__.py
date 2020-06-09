from .auth import routes as auth_routes
from .profiles import routes as profiles_routes
from .posts import routes as posts_routes
from .comments import routes as comments_routes

ROUTES = auth_routes + \
    profiles_routes + \
    posts_routes + \
    comments_routes


def init_routes(api):
    for route in ROUTES:
        api.add_resource(route[0], f"/v1{route[1]}")
