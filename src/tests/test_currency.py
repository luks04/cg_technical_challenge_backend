import sys
sys.path.append('../')
import pytest
import json
import datetime
from flask_jwt_extended import create_access_token
from modules.currency import serialize_input
from shared.constants import *
from http import HTTPStatus
from app import app

class TestApiCurrencyCurrentExchangeRate:
    def test_api_currency_get_current_exchange_rate(self):
        with app.app_context():
            access_token = create_access_token(identity = -1, 
                                               additional_claims = {"max_requests": MAX_REQUESTS})
            headers = {
                'Authorization': f'Bearer {access_token}'
            }
            body_request = {'fixer_access_key': None, 'bmx_token': None}
            response = app.test_client().post(
                '/api/currency/get_current_exchange_rate',
                headers = headers,
                data = json.dumps(body_request),
                content_type = 'application/json',
            )
            json_response = json.loads(response.get_data(as_text = True))
            assert json_response['msg'] == GET_CURRENT_EXCHANGE_RATES_SUCCESS
            assert json_response['details']['max_requests'] == MAX_REQUESTS
            rates = json_response['rates']
            assert len(rates) == 3
            for rate in rates:
                assert 'data' in rate.keys()
                assert 'details' in rate.keys()
                assert 'success' in rate.keys()
                if rate['success']:
                    assert datetime.datetime.strptime(rate['data']['date'], '%d-%m-%Y')
                    assert type(rate['data']['value']) == float
                    assert rate['details']['msg'] == REQUEST_3RD_PARTY_SOURCE_SUCCESS
                else:
                    assert rate['data'] is None
            assert response._status_code == HTTPStatus.OK

class TestSerializeInput:
    @pytest.mark.parametrize('input_test', ['', ' ', None])
    def test_serialize_input_None(self, input_test):
        serialized_input = serialize_input(input_test)
        assert serialized_input is None
    
    @pytest.mark.parametrize('input_test', [' fake_input', 'fake_input ', ' fake_input '])
    def test_serialize_input_not_None(self, input_test):
        serialized_input = serialize_input(input_test)
        assert serialized_input != input_test
