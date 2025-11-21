from marshmallow import Schema, fields
from src.schemas.base import PaginationRequestSchema, PaginationResponseSchema


class ExpenseSchema(Schema):
    id = fields.Int(dump_only=True)
    amount = fields.Float(required=True)
    note = fields.Str()
    category_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    deleted_at = fields.DateTime(dump_only=True)
    user_id = fields.Int(dump_only=True)


class UpdateExpenseSchema(Schema):
    amount = fields.Float()
    note = fields.Str()
    category_id = fields.Int()


class ExpenseRequestSchema(PaginationRequestSchema):
    start_date = fields.DateTime()
    end_date = fields.DateTime()
    category_ids = fields.List(fields.Int())


class ExpenseResponseSchema(PaginationResponseSchema):
    data = fields.List(fields.Nested(ExpenseSchema))
