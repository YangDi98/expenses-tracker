from flask import Flask, jsonify
from flask_smorest import Api
from http import HTTPStatus
from datetime import timedelta
from dotenv import load_dotenv
from typing import Optional
import os

from src.extensions import db, migrate, bcrypt, jwt
from src.views.expenses import blueprint as ExpenseBlueprint
from src.views.auth import blueprint as AuthBlueprint
from src.models.users import User


def error_message(
    status: HTTPStatus,
    error: str,
    message: str,
    details: Optional[dict] = None,
):
    response = {
        "status": status.value,
        "error": error,
        "message": message,
    }
    if details:
        response["details"] = details
    return jsonify(response), status


def register_jwt_handlers(jwt):
    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return str(user.id)

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        user = User.get_by_id(int(identity))
        if user and (not user.active or user.deleted_at is not None):
            return None
        return user

    @jwt.unauthorized_loader
    def handle_unauthorized_error(err):
        return error_message(
            HTTPStatus.UNAUTHORIZED,
            "Unauthorized",
            "Account is inactive or has been deleted",
        )

    @jwt.user_lookup_error_loader
    def handle_user_lookup_error(_jwt_header, _jwt_payload):
        return error_message(
            HTTPStatus.UNAUTHORIZED,
            "Unauthorized",
            "Account is inactive or has been deleted",
        )


def create_app(config: Optional[dict] = None):
    load_dotenv()
    app = Flask("Flask Expense Tracker API")
    app.config["API_TITLE"] = "Flask Expense Tracker API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.2"

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///expenses_db.sqlite"
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)
    app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
    app.config["JWT_REFRESH_COOKIE_PATH"] = "/auth/refresh"
    app.config["JWT_COOKIE_CSRF_PROTECT"] = True

    if config:
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    from src import models  # noqa: F401

    @app.errorhandler(HTTPStatus.UNPROCESSABLE_ENTITY)
    def handle_unprocessable_entity(err):
        return error_message(
            HTTPStatus.BAD_REQUEST,
            "Bad Request",
            "Invalid request",
            err.exc.messages if hasattr(err, "exc") else None,
        )

    register_jwt_handlers(jwt)

    api = Api(app)
    api.register_blueprint(ExpenseBlueprint)
    api.register_blueprint(AuthBlueprint)

    return app
