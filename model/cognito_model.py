from typing import TypedDict

from marshmallow import Schema, fields


class CognitoModel:
    def __init__(self, region: str, client_id: str, endpoint_port: str):
        self._region: str = region
        self._client_id: str = client_id
        self._endpoint_port: str = endpoint_port

    def get_region(self) -> str:
        return self._region

    def get_client_id(self) -> str:
        return self._client_id

    def get_endpoint_port(self) -> str:
        return self._endpoint_port


class CognitoSchema(Schema):
    region = fields.Str(required=True)
    client_id = fields.Str(required=True)
    endpoint_port = fields.Str(required=True)


class CognitoData(TypedDict):
    region: str
    client_id: str
    endpoint_port: str
