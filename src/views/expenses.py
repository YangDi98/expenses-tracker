from flask_smorest import Blueprint
from http import HTTPStatus
from flask import url_for

from src.models.expenses import Expense
from src.schemas.expenses import (
    ExpenseSchema,
    UpdateExpenseSchema,
    ExpenseRequestSchema,
    ExpenseResponseSchema,
)

blueprint = Blueprint(
    "expenses",
    __name__,
    url_prefix="/expenses",
    description="Operations on expenses",
)


@blueprint.route("/", methods=["GET"])
@blueprint.response(HTTPStatus.OK, schema=ExpenseSchema(many=True))
@blueprint.arguments(ExpenseRequestSchema, location="query")
@blueprint.response(HTTPStatus.OK, schema=ExpenseResponseSchema)
def get_expenses(args):
    expenses = Expense.filter(**args)
    args.pop("cursor_created_at", None)
    args.pop("cursor_id", None)
    url = (
        url_for(
            "expenses.get_expenses",
            cursor_created_at=expenses[-1].created_at,
            cursor_id=expenses[-1].id,
            **args,
            _external=True,
        )
        if expenses
        else None
    )
    return {"data": expenses, "next_url": url}


@blueprint.route("/<int:expense_id>", methods=["GET"])
@blueprint.response(HTTPStatus.OK, schema=ExpenseSchema)
def get_expense(expense_id):
    expense = Expense.get_by_id_or_404(expense_id)
    return expense


@blueprint.route("/", methods=["POST"])
@blueprint.arguments(ExpenseSchema, location="json")
@blueprint.response(HTTPStatus.CREATED, schema=ExpenseSchema)
def create_expense(expense_data):
    expense = Expense(**expense_data)
    expense.save(commit=True)
    return expense


@blueprint.route("/<int:expense_id>", methods=["PUT"])
@blueprint.arguments(UpdateExpenseSchema, location="json")
@blueprint.response(HTTPStatus.OK, schema=ExpenseSchema)
def update_expense(expense_data, expense_id):
    expense = Expense.get_by_id_or_404(expense_id)
    expense.update(expense_data, commit=True)
    return expense


@blueprint.route("/<int:expense_id>", methods=["DELETE"])
@blueprint.response(HTTPStatus.NO_CONTENT)
def delete_expense(expense_id):
    expense = Expense.get_by_id_or_404(expense_id)
    expense.soft_delete(commit=True)
    return "", HTTPStatus.NO_CONTENT
