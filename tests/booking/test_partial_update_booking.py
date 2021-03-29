import pytest
from booking_service import Booking, BookingAuth

import json
import pytest
import allure


class TestUpdateBooking:
    @pytest.fixture
    def setup(self, base_url: str, pytestconfig):
        self.url = base_url
        self.booking: Booking = Booking(base_url)
        self.body: dict = {}

        username: str = pytestconfig.getoption('username')
        password: str = pytestconfig.getoption('password')
        self.creds: dict = {'username': username, 'password': password}

        with open('data/booking.json', 'r') as f:
            self.body = json.load(f)

        resp = self.booking.create_booking(
            json=self.body,
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        )

        with allure.step('Create booking for test'):
            self.booking_id = resp.json().get('bookingid')
        yield
        # no delete booking teardown since service is restarted every 10 minutes


    def test_partial_update_booking_should_be_success(self, setup):
        token_id: str = BookingAuth(self.url).auth(json=self.creds, headers={'Content-Type': 'application/json'}).json().get('token')

        update_json = {
                "firstname" : "James",
                "lastname" : "Brown",
        }

        with allure.step('Update booking'):
            resp = self.booking.partial_update_booking(
                booking_id=self.booking_id,
                json=update_json,
                headers={
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'Cookie': f'token={token_id}'
                }
            )

        with allure.step('Get status code'):
            assert resp.status_code == 200

        with allure.step('Check updated booking was updated correctly'):
            self.body['firstname'] = 'James'
            self.body['lastname'] = 'Brown'
            created_booking = self.booking.get_booking(self.booking_id)
            assert created_booking.json() == self.body


    def test_partial_update_booking_without_auth_should_be_failed(self, setup):

        update_json = {
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

        resp = self.booking.partial_update_booking(
            booking_id=self.booking_id,
            json=update_json,
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            }
        )

        assert resp.status_code == 403
