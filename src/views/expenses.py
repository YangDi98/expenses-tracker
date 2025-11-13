from flask_smorest import Blueprint
from http import HTTPStatus
from flask import url_for, request
from flask_jwt_extended import jwt_required

from src.models.expenses import Expense
from src.models.categories import Category
from src.schemas.expenses import (
    ExpenseSchema,
    UpdateExpenseSchema,
    ExpenseRequestSchema,
    ExpenseResponseSchema,
)
from src.views.utils import user_access_required

blueprint = Blueprint(
    "expenses",
    __name__,
    url_prefix="/users/<int:user_id>/expenses",
    description="Operations on expenses",
)


@blueprint.route("/", methods=["GET"])
@blueprint.response(HTTPStatus.OK, schema=ExpenseSchema(many=True))
@blueprint.arguments(ExpenseRequestSchema, location="query")
@blueprint.response(HTTPStatus.OK, schema=ExpenseResponseSchema)
@jwt_required()
@user_access_required
def get_expenses(args, user_id):
    expenses = Expense.filter(user_id=user_id, **args)
    args.pop("cursor_created_at", None)
    args.pop("cursor_id", None)
    next_cursor_id = expenses[-1].id if expenses else None
    next_cursor_created_at = expenses[-1].created_at if expenses else None
    url = None
    if (next_cursor_id or next_cursor_created_at) and request.endpoint:
        url = (
            url_for(
                request.endpoint,
                user_id=user_id,
                cursor_created_at=next_cursor_created_at,
                cursor_id=next_cursor_id,
                **args,
                _external=True,
            )
            if expenses
            else None
        )
    return {"data": expenses, "next_url": url}


@blueprint.route("/<int:expense_id>", methods=["GET"])
@blueprint.response(HTTPStatus.OK, schema=ExpenseSchema)
@jwt_required()
@user_access_required
def get_expense(user_id, expense_id):
    expense = Expense.get_by_user_id_and_id_or_404(user_id, expense_id)
    return expense


@blueprint.route("/", methods=["POST"])
@blueprint.arguments(ExpenseSchema, location="json")
@blueprint.response(HTTPStatus.CREATED, schema=ExpenseSchema)
@jwt_required()
@user_access_required
def create_expense(expense_data, user_id):
    Category.get_by_user_id_and_id_or_404(user_id, expense_data["category_id"])
    expense = Expense(**expense_data)
    expense.save(commit=True)
    return expense


@blueprint.route("/<int:expense_id>", methods=["PUT"])
@blueprint.arguments(UpdateExpenseSchema, location="json")
@blueprint.response(HTTPStatus.OK, schema=ExpenseSchema)
@jwt_required()
@user_access_required
def update_expense(expense_data, user_id, expense_id):
    Category.get_by_user_id_and_id_or_404(user_id, expense_data["category_id"])
    expense = Expense.get_by_user_id_and_id_or_404(user_id, expense_id)
    expense.update(expense_data, commit=True)
    return expense


@blueprint.route("/<int:expense_id>", methods=["DELETE"])
@blueprint.response(HTTPStatus.NO_CONTENT)
@jwt_required()
@user_access_required
def delete_expense(user_id, expense_id):
    expense = Expense.get_by_user_id_and_id_or_404(user_id, expense_id)
    expense.soft_delete(commit=True)
    return "", HTTPStatus.NO_CONTENT
