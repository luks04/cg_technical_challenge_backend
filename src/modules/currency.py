__author__ = "Lucas A. Patino"
__version__ = "1.0.0"
__mantainer__ = "Lucas A. Patino"

import os
import json
from flask import Blueprint
from flask import Response
from flask import jsonify
from flask import request
from flask_cors import CORS
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt
from dotenv import load_dotenv
from http import HTTPStatus
from typing import Union
from models.BanxicoData import BanxicoData
from models.FixerData import FixerData
from models.FederationJournalData import FederationJournalData
from shared.constants import *

# Load .env file ENV variables
load_dotenv()

# Initial configuration
currency = Blueprint('currency', __name__)

# CORS configuration
CORS(currency, resources = {r"/api/currency/*": {
    "origins": json.loads(os.environ.get('ALLOWED_ORIGINS')), 
    "methods": ["POST"]
    }})
    
########################### CURRENT EXCHANGE AREA START ###########################

def serialize_input(input: Union[str, None]) -> Union[str, None]:
    """It returns None if the input is empty. Otherwise it returns the 
    input after removing leading and trailing whitespace.

    Args:
    -----
        input (Union[str, None]): Could be None or any string.

    Returns:
        Union[str, None]: Serialized input.
    """
    if input is not None:
        input = input.strip()
        if input == '':
            return None
    return input

@currency.route("/api/currency/get_current_exchange_rate", methods = ['GET', 'POST'])
@jwt_required()
def api_currency_get_current_exchange_rate() -> Response:
    try:
        # Get received data
        fixer_access_key = serialize_input(request.json.get("fixer_access_key", None))
        bmx_token = serialize_input(request.json.get("bmx_token", None))
        # Get jwt token
        jwt_token = get_jwt()
        # Get data from multiple exchange rate sources:
        federation_journal_data = FederationJournalData()
        fixer_data = FixerData(fixer_access_key)
        banxico_data = BanxicoData(bmx_token)
        federation_journal_data.set_federation_journal_data()
        fixer_data.set_fixer_data()
        banxico_data.set_banxico_data()
        # Build current exchange rates from all sources
        rates_data = list()
        rates_data.append(federation_journal_data.get_service_response())
        rates_data.append(fixer_data.get_service_response())
        rates_data.append(banxico_data.get_service_response())
        # Create the response
        response = jsonify({'msg': GET_CURRENT_EXCHANGE_RATES_SUCCESS, 
                            'details': {'max_requests': jwt_token["max_requests"]},
                            'rates': rates_data
                            })
        response.status = HTTPStatus.OK
    except Exception as error:
        print(error)
        # Create an exception response
        response = jsonify({'msg': DEFAULT_EXCEPTION_MSG, 
                            'error': str(error)
                            })
        response.status = HTTPStatus.INTERNAL_SERVER_ERROR
    finally:
        return response

########################### CURRENT EXCHANGE AREA END ###########################
