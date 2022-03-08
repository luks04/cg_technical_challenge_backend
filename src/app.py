import os
import json
from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from dotenv import load_dotenv
from http import HTTPStatus
from models.User import User
from shared.constants import *

# Load .env file ENV variables
load_dotenv()

# Initial configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config["JWTSECRETKEY"] = "secret"
jwt = JWTManager(app)

# CORS configuration
CORS(app, resources = {r"/api/app/*": {
    "origins": json.loads(os.environ.get('ALLOWED_ORIGINS')), 
    "methods": ["POST"]
    }})


########################### AUTHENTICATION AREA START ###########################
def valid_fake_username_and_password(user: User) -> bool:
    """Simulate credentials verification.

    Args:
    -----
        user (User): User object to verify

    Returns:
    --------
        bool: Returns True if username and password are 'admin', False otherwise.
    """
    fake_verifation = user.username == 'admin' and user.password == 'admin'
    return fake_verifation

@app.route("/api/app/login", methods = ["POST"])
def api_app_login():
    """If the user exists, it returns a valid access_token.
    Otherwise, it returns an error message.
    
    Returns:
    --------
        str: The jsonify response with its respective status code
    """
    try:
        # Get received data
        username = request.json.get("username", None)
        password = request.json.get("password", None)
        # Check if username or password are None
        if username is None or password is None:
            # Create a failed auth response
            response = jsonify({'msg': AUTH_FAILED, 
                                'detail': AUTH_FAILED_DETAIL
                                })
            response.status = HTTPStatus.BAD_REQUEST
        # Creates User object
        user = User(username, password)
        # Fake credentials verification
        are_valid_credentials = valid_fake_username_and_password(user)
        if are_valid_credentials:
            # Creates the access_token with a fake identity (ID) and max_requests per user
            access_token = create_access_token(identity = 1, 
                                               additional_claims = {"max_requests": MAX_REQUESTS})
            response = jsonify({'msg': AUTH_SUCCESS, 
                                'detail': AUTH_SUCCESS_DETAIL,
                                'token': access_token
                                })
            response.status = HTTPStatus.OK
        else:
            # Create a failed auth response
            response = jsonify({'msg': AUTH_FAILED, 
                                'detail': AUTH_FAILED_DETAIL
                                })
            response.status = HTTPStatus.UNAUTHORIZED
    except Exception as error:
        # Create an exception response
        response = jsonify({'msg': DEFAULT_EXCEPTION_MSG, 
                            'detail': str(error)
                            })
        response.status = HTTPStatus.INTERNAL_SERVER_ERROR
    finally:
        return response

########################### AUTHENTICATION AREA END ###########################

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8080, debug = True)
