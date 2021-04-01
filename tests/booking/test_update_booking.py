import pytest
from booking_service import Booking, BookingAuth

import json
import pytest
from requests.models import Response

class TestUpdateBooking:
    @pytest.fixture
    def setup(self, base_url: str, pytestconfig):
        self.url: str = base_url
        self.booking: Booking = Booking(base_url)
        body: dict = {}

        username: str = pytestconfig.getoption('username')
        password: str = pytestconfig.getoption('password')
        self.creds: dict = {'username': username, 'password': password}

        with open('data/booking.json', 'r') as f:
            body = json.load(f)

        resp: Response = self.booking.create_booking(
            json=body,
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        )

        self.booking_id = resp.json().get('bookingid')
        yield
        # no delete booking teardown since service is restarted every 10 minutes

    def test_update_booking_should_be_success(self, setup):
        token_id: str = BookingAuth(self.url).auth(json=self.creds, headers={'Content-Type': 'application/json'}).json().get('token')

        update_json: dict = {
                "firstname" : "James",
                "lastname" : "Brown",
                "totalprice" : 111,
                "depositpaid" : True,
                "bookingdates" : {
                    "checkin" : "2022-01-01",
                    "checkout" : "2023-01-01"
                },
                "additionalneeds" : "Girl"
        }

        resp: Response = self.booking.update_booking(
            booking_id=self.booking_id,
            json=update_json,
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Cookie': f'token={token_id}'
            }
        )

        assert resp.status_code == 200

        resp = self.booking.get_booking(self.booking_id)
        assert resp.json() == update_json

    def test_update_booking_without_auth_should_be_fail(self, setup):

        update_json: dict = {
                "firstname" : "James",
                "lastname" : "Brown",
                "totalprice" : 111,
                "depositpaid" : True,
                "bookingdates" : {
                    "checkin" : "2022-01-01",
                    "checkout" : "2023-01-01"
                },
                "additionalneeds" : "Girl"
        }

        resp: Response = self.booking.update_booking(
            booking_id=self.booking_id,
            json=update_json,
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            }
        )

        assert resp.status_code == 403
