class InternalServerError(Exception):
    pass


class SchemaValidationError(Exception):
    pass


class UsernameAlreadyExistsError(Exception):
    pass


class EmailAlreadyExistsError(Exception):
    pass


class UnauthorizedError(Exception):
    pass


class PostNotFoundError(Exception):
    pass


class CommentNotFoundError(Exception):
    pass


errors = {
    "InternalServerError": {
        "message": "Something went wrong",
        "status": 500
    },
    "SchemaValidationError": {
        "message": "Request is missing required fields",
        "status": 400
    },
    "UsernameAlreadyExistsError": {
        "message": "Movie with given name already exists",
        "status": 400
    },
    "EmailAlreadyExistsError": {
        "message": "User with given email address already exists",
        "status": 400
    },
    "UnauthorizedError": {
        "message": "Invalid email or password",
        "status": 401
    },
    "CommentNotFoundError": {
        "message": "Comment not found",
        "status": 404
    },
    "PostNotFoundError": {
        "message": "Post not found",
        "status": 404
    }
}
