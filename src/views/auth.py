from flask_smorest import Blueprint, abort
from flask import jsonify
from http import HTTPStatus
from sqlalchemy import or_
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    set_refresh_cookies,
    jwt_required,
    current_user,
)
from src.schemas.auth import (
    RegisterRequestSchema,
    UserSchema,
    LoginRequestSchema,
)
from src.models.users import User
from src.extensions import db, bcrypt

blueprint = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth",
    description="Operations on authentication",
)


@blueprint.route("/register", methods=["POST"])
@blueprint.arguments(RegisterRequestSchema, location="json")
@blueprint.response(201, schema=UserSchema)
def register_user(req_json):
    stmt = User.select_active().where(
        or_(
            User.username == req_json["username"].lower(),
            User.email == req_json["email"].lower(),
        )
    )
    existing_user = db.session.execute(stmt).scalar_one_or_none()
    if existing_user:
        abort(HTTPStatus.CONFLICT, message="Username or email already exists")
    hashed = bcrypt.generate_password_hash(req_json.pop("password")).decode(
        "utf-8"
    )
    user = User.create({**req_json, "password_hash": hashed})
    return user


@blueprint.route("/login", methods=["POST"])
@blueprint.arguments(LoginRequestSchema, location="json")
def login_user(req_json):
    user = User.get_by_username_or_email(req_json["login"])

    if not user:
        abort(HTTPStatus.UNAUTHORIZED, message="Invalid credentials")
    if not bcrypt.check_password_hash(
        user.password_hash, req_json["password"]
    ):
        abort(HTTPStatus.UNAUTHORIZED, message="Invalid credentials")
    if not user.active:
        abort(HTTPStatus.UNAUTHORIZED, message="Account is deactivated")
    access_token = create_access_token(identity=user)
    refresh_token = create_refresh_token(identity=user)
    response = jsonify(
        {
            "access_token": access_token,
        }
    )
    set_refresh_cookies(response, refresh_token)
    return response, HTTPStatus.OK


@blueprint.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh_token():
    access_token = create_access_token(identity=current_user)
    return (
        jsonify(
            {
                "access_token": access_token,
            }
        ),
        HTTPStatus.OK,
    )


@blueprint.route("/who_am_i", methods=["GET"])
@jwt_required()
def protected():
    # We can now access our sqlalchemy User object via `current_user`.
    return jsonify(
        id=current_user.id,
        username=current_user.username,
    )
