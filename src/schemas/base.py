from marshmallow import Schema, fields


class PaginationRequestSchema(Schema):
    limit = fields.Int(load_default=100)
    cursor_created_at = fields.DateTime()
    cursor_id = fields.Int()


class PaginationResponseSchema(Schema):
    next_url = fields.Str()
