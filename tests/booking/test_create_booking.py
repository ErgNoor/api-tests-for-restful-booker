from typing import Optional
from requests.models import Response
from booking_service import Booking, BookingAuth

import json
import pytest
import logging


logging.basicConfig(
    level=logging.INFO,
)
create_booking_logger = logging.getLogger(__name__)


class TestCreateBooking:
    @pytest.fixture
    def setup(self, base_url, pytestconfig):
        self.booking = Booking(base_url)
        self.booking_id: Optional[int] = None
        yield
        username: str = pytestconfig.getoption('username')
        password: str = pytestconfig.getoption('password')
        creds: dict = {'username': username, 'password': password}

        token_id = BookingAuth(base_url).auth(json=creds, headers={'Content-Type': 'application/json'})
        print(token_id)
        self.booking.delete_booking(
            self.booking_id,
            headers =
            {
                'Content-Type': 'application/json',
                'Cookie': f'token={token_id}'
            }
        )

    def test_create_booking_should_be_success(self, setup):
        body = {}
        with open('data/booking.json', 'r') as f:
            body = json.load(f)

        resp = self.booking.create_booking(
            json=body,
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        )

        self.booking_id = resp.json().get('bookingid')

        assert resp.status_code == 200, f'Incorrect status code. Got {resp.status_code}'
        assert resp.json().get('booking') == body

    def test_create_booking__without_headers_should_be_success(self, setup):
        body = {}
        with open('data/booking.json', 'r') as f:
            body = json.load(f)

        resp = self.booking.create_booking(
            json=body,
        )

        self.booking_id = resp.json().get('bookingid')

        assert resp.status_code == 200, f'Incorrect status code. Got {resp.status_code}'
        assert resp.json().get('booking') == body
