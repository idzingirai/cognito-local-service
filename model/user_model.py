from typing import TypedDict

from marshmallow import Schema, fields


class UserModel:
    def __init__(self, username: str, password: str):
        self._username: str = username
        self._password: str = password

    def get_username(self) -> str:
        return self._username

    def get_password(self) -> str:
        return self._password


class UserSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class UserData(TypedDict):
    username: str
    password: str
