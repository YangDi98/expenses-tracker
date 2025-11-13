from marshmallow import Schema, fields, ValidationError, pre_load
import re


def validate_password(password: str):
    reg = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$#%])[A-Za-z\d@$#%]{9,}$"
    pat = re.compile(reg)

    mat = re.search(pat, password)

    # Have at least one number
    # Have at least one uppercase letter
    # Have at least one lowercase letter
    # Have at least one special character

    if not mat:
        raise ValidationError("Invalid Password")


class RegisterRequestSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)

    @pre_load
    def validate_input(self, data, **kwargs):
        fields = ["email", "first_name", "last_name", "username"]
        for field in fields:
            data[field] = data.get(field, "").strip()
            if not data[field]:
                raise ValidationError(
                    f"{field.replace('_', ' ').title()} "
                    f"cannot be empty or just spaces"
                )
        data["username"] = data["username"].lower()
        data["email"] = data["email"].lower()
        reg_email = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        pat_email = re.compile(reg_email)
        mat_email = re.search(pat_email, data["email"])
        if not mat_email:
            raise ValidationError("Invalid Email Address")
        validate_password(data.get("password", ""))
        return data


class LoginRequestSchema(Schema):
    login = fields.Str(
        required=True, metadata={"description": "Username or email"}
    )
    password = fields.Str(required=True)

    @pre_load
    def validate_input(self, data, **kwargs):
        data["login"] = data.get("login", "").strip().lower()
        if not data["login"]:
            raise ValidationError("Username or email cannot be empty")
        if not data.get("password"):
            raise ValidationError("Password cannot be empty")
        return data


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    active = fields.Bool(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    deleted_at = fields.DateTime(dump_only=True)
