import sys
sys.path.append('../')
import pytest
import json
from models.User import User
from shared.constants import *
from http import HTTPStatus
from app import app
from app import valid_fake_username_and_password

class TestApiLogin:
    body_request_cases = [
        {'username': 'fake_user', 'password': 'fake_password'},
        {'username': None, 'password': ''},
        {},
    ]
    
    def test_api_app_login_success(self):
        body_request = {'username': 'admin', 'password': 'admin'}
        response = app.test_client().post(
            '/api/app/login',
            data = json.dumps(body_request),
            content_type = 'application/json',
        )
        json_response = json.loads(response.get_data(as_text = True))
        assert json_response['msg'] == AUTH_SUCCESS
        assert json_response['detail'] == AUTH_SUCCESS_DETAIL
        assert response._status_code == HTTPStatus.OK
    
    @pytest.mark.parametrize('body_requests', body_request_cases)
    def test_api_app_login_fail(self, body_requests):
        response = app.test_client().post(
            '/api/app/login',
            data = json.dumps(body_requests),
            content_type = 'application/json',
        )
        json_response = json.loads(response.get_data(as_text = True))
        assert json_response['msg'] == AUTH_FAILED
        assert json_response['detail'] == AUTH_FAILED_DETAIL
        assert response._status_code == HTTPStatus.UNAUTHORIZED
    
    def test_api_app_login_server_error(self):
        body_request = None
        response = app.test_client().post(
            '/api/app/login',
            data = json.dumps(body_request),
            content_type = 'application/json',
        )
        json_response = json.loads(response.get_data(as_text = True))
        assert json_response['msg'] == DEFAULT_EXCEPTION_MSG
        assert response._status_code == HTTPStatus.INTERNAL_SERVER_ERROR

class TestValidFakeUsernameAndPassword:
    def test_valid_fake_username_and_password(self):
        user = User("admin", "admin")
        response = valid_fake_username_and_password(user)
        assert response
        
    def test_wrong_fake_username_and_password(self):
        user = User("", "")
        response = valid_fake_username_and_password(user)
        assert not response
