from requests.api import delete
from booking_service import Booking, BookingAuth

import pytest

import json
from requests.models import Response

from typing import Optional
import logging


logging.basicConfig(
    level=logging.INFO,
)
delete_booking_logger = logging.getLogger(__name__)


class TestDeleteBooking:
    @pytest.fixture
    def setup(self, base_url, pytestconfig):
        self.url = base_url
        self.booking = Booking(base_url)
        username: str = pytestconfig.getoption('username')
        password: str = pytestconfig.getoption('password')
        self.creds: dict = {'username': username, 'password': password}

        body: dict = {}

        with open('data/booking.json', 'r') as f:
            body = json.load(f)

        create_resp: Response = self.booking.create_booking(
            json=body,
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        )

        self.booking_id = create_resp.json().get('bookingid')
        # print(booking_id)
        delete_booking_logger.info(f'booking with {self.booking_id=} was created successful')
        yield

    def test_delete_booking_without_authorisation_should_be_fail(self, setup):
        resp = self.booking.delete_booking(self.booking_id)
        
        assert resp.status_code == 403, f'Incorrect status code. Got {resp.status_code}'


    def test_delete_booking_with_cookie_auth_should_be_success(self, setup):
        token_id: str = BookingAuth(self.url).auth(json=self.creds, headers={'Content-Type': 'application/json'}).json().get('token')
        print(token_id)

        resp = self.booking.delete_booking(
            self.booking_id,
            headers =
            {
                'Content-Type': 'application/json',
                'Cookie': f'token={token_id}'
            }
        )
        
        assert resp.status_code == 201, f'Incorrect status code. Got {resp.status_code}'


    @pytest.mark.xfail(reason='Basic auth not implemented')
    def test_delete_booking_with_basic_auth_should_be_success(self, setup):
        token_id: str = BookingAuth(self.url).auth(json=self.creds, headers={'Content-Type': 'application/json'}).json().get('token')
        print(token_id)
        
        resp = self.booking.delete_booking(
            self.booking_id,
            headers =
            {
                'Content-Type': 'application/json',
                'Authorisation': f'Basic {token_id}'
            }
        )
        
        assert resp.status_code == 200, f'Incorrect status code. Got {resp.status_code}'
