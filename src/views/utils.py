from flask_jwt_extended import current_user
from flask import jsonify
from http import HTTPStatus


def user_access_required(func):
    def wrapper(*args, **kwargs):
        if not current_user or (
            not current_user.active or current_user.deleted_at is not None
        ):
            return (
                jsonify({"message": "User account is inactive or not found"}),
                HTTPStatus.UNAUTHORIZED,
            )

        if "user_id" in kwargs:
            user_id = kwargs["user_id"]
            if current_user.id != user_id:
                return (
                    jsonify(
                        {
                            "message": "User does not have "
                            "permission to access this resource"
                        }
                    ),
                    HTTPStatus.FORBIDDEN,
                )

        return func(*args, **kwargs)

    return wrapper
