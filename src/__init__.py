from flask import Flask
from flask_smorest import Api
from http import HTTPStatus

from src.extensions import db, migrate
from src.views.expenses import blueprint as ExpenseBlueprint


def create_app():
    app = Flask("Flask Expense Tracker API")
    app.config["API_TITLE"] = "Flask Expense Tracker API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.2"

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///expenses_db.sqlite"
    db.init_app(app)
    migrate.init_app(app, db)

    from src import models  # noqa: F401

    @app.errorhandler(HTTPStatus.UNPROCESSABLE_ENTITY)
    def handle_unprocessable_entity(err):
        return {
            "message": "Invalid request",
            "errors": err.data.get("messages", {}),
        }, HTTPStatus.BAD_REQUEST

    api = Api(app)
    api.register_blueprint(ExpenseBlueprint)

    return app
