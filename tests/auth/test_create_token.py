from conftest import base_url
from requests.models import Response
from booking_service import BookingAuth

import pytest


class TestBookingAuth:
    @pytest.fixture
    def setup(self, base_url):
        self.booking_auth = BookingAuth(base_url)
        yield

    def test_token_should_be_created_success(self, setup, credentials: dict) -> None:
        response = self.booking_auth.auth(json=credentials, headers={'Content-Type': 'application/json'})
        
        assert response.status_code == 200, f'Incorrect status code. Got {response.status_code}'
        assert 'token' in response.json().keys(), 'No token in response'

    def test_token_request_without_credentials_should_fail(self, setup) -> None:
        response = self.booking_auth.auth(headers={'Content-Type': 'application/json'})
        
        assert response.status_code == 200, f'Incorrect status code. Got {response.status_code}'
        assert response.json() == {'reason': 'Bad credentials'}

    def test_token_request_without_headers_and_credentials_should_fail(self, setup) -> None:
        response = self.booking_auth.auth()
        
        assert response.status_code == 200, f'Incorrect status code. Got {response.status_code}'
        assert response.json() == {'reason': 'Bad credentials'}

    def test_token_request_with_credentials_and_without_headers_should_fail(self, setup, credentials: dict) -> None:
        response = self.booking_auth.auth(json=credentials)
        
        assert response.status_code == 200, f'Incorrect status code. Got {response.status_code}'
        assert 'token' in response.json().keys(), 'No token in response'