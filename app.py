import boto3
from flask import Flask, request, jsonify

from model.cognito_model import CognitoSchema, CognitoModel
from model.user_model import UserModel, UserData, UserSchema


REGION = None
CLIENT_ID = None
CLIENT = None


def initialize_cognito_variables(request_json: dict):
    cognito_schema: CognitoSchema = CognitoSchema()
    cognito_data = cognito_schema.load(request_json)
    cognito_model: CognitoModel = CognitoModel(**cognito_data)

    global REGION, CLIENT_ID, CLIENT
    REGION = cognito_model.get_region()
    CLIENT_ID = cognito_model.get_client_id()
    CLIENT = boto3.client(
        'cognito-idp',
        region_name=REGION,
        endpoint_url=f'http://host.docker.internal:{cognito_model.get_endpoint_port()}'
    )


def retrieve_tokens(request_json: dict) -> dict:
    user_schema: UserSchema = UserSchema()
    user_data: UserData = user_schema.load(request_json)
    user_model: UserModel = UserModel(**user_data)

    authentication_response: dict = CLIENT.initiate_auth(
        ClientId=CLIENT_ID,
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            'USERNAME': user_model.get_username(),
            'PASSWORD': user_model.get_password()
        }
    )

    return authentication_response['AuthenticationResult']


app = Flask(__name__)


@app.route('/config', methods=['POST'])
def setup_cognito_variables():
    initialize_cognito_variables(request.json)
    return jsonify({"message": "Cognito variables initialized successfully"}), 200


@app.route('/tokens', methods=['POST'])
def get_tokens():
    tokens = retrieve_tokens(request.json)
    return tokens


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
