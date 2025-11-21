from flask_smorest import Blueprint
from http import HTTPStatus
from flask_jwt_extended import jwt_required

from src.models.categories import Category
from src.schemas.categories import CategorySchema
from src.views.utils import user_access_required

blueprint = Blueprint(
    "categories",
    __name__,
    url_prefix="/users/<int:user_id>/categories",
    description="Operations on categories",
)


@blueprint.route("/", methods=["GET"])
@blueprint.response(HTTPStatus.OK, schema=CategorySchema(many=True))
@jwt_required()
@user_access_required
def get_categories(user_id):
    categories = Category.query.filter_by(
        user_id=user_id, deleted_at=None
    ).all()
    return categories


@blueprint.route("/<int:category_id>", methods=["GET"])
@blueprint.response(HTTPStatus.OK, schema=CategorySchema)
@jwt_required()
@user_access_required
def get_category(user_id, category_id):
    category = Category.query.filter_by(
        id=category_id, user_id=user_id, deleted_at=None
    ).first_or_404()
    return category


@blueprint.route("/", methods=["POST"])
@blueprint.arguments(CategorySchema, location="json")
@blueprint.response(HTTPStatus.CREATED, schema=CategorySchema)
@jwt_required()
@user_access_required
def create_category(new_category_data, user_id):
    new_category = Category.create({**new_category_data, "user_id": user_id})
    new_category.save()
    return new_category, HTTPStatus.CREATED
