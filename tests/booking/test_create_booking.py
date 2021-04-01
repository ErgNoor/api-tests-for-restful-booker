from typing import Optional
from requests.models import Response
from booking_service import Booking, BookingAuth

import json
import pytest
import logging
import allure


logging.basicConfig(
    level=logging.INFO,
)
create_booking_logger = logging.getLogger(__name__)


@allure.story('Tests for create booking')
class TestCreateBooking:
    @pytest.fixture
    def setup(self, base_url: str, pytestconfig):
        with allure.step('Create Booking object'):
            self.booking: Booking = Booking(base_url)

        self.booking_id: Optional[int] = None
        yield
        username: str = pytestconfig.getoption('username')
        password: str = pytestconfig.getoption('password')
        creds: dict = {'username': username, 'password': password}

        with allure.step('Get token'):
            token = BookingAuth(base_url).auth(json=creds, headers={'Content-Type': 'application/json'}).json().get('token')

            create_booking_logger.info(f'{token=}')

        with allure.step('Delete created booking'):
            delete_resp: Response = self.booking.delete_booking(
                self.booking_id,
                headers =
                {
                    'Content-Type': 'application/json',
                    'Cookie': f'token={token}'
                }
            )

        with allure.step('Checking delete response'):
            if delete_resp.status_code == 201:
                create_booking_logger.info(f'Booking with booking id = {self.booking_id} should be deleted')
            else:
                create_booking_logger.info(f'Booking with booking id = {self.booking_id} was not deleted')

    @allure.feature('Create booking')
    def test_create_booking_should_be_success(self, setup):
        body: dict = {}

        with allure.step('Open booking.json'):
            with open('data/booking.json', 'r') as f:
                body = json.load(f)

        with allure.step('Create booking'):
            resp: Response = self.booking.create_booking(
                json=body,
                headers={
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            )

        with allure.step('Get booking id'):
            self.booking_id = resp.json().get('bookingid')

        with allure.step('Checking status code'):
            assert resp.status_code == 200, f'Incorrect status code. Got {resp.status_code}'

        with allure.step('Check booking was created with correct body'):
            assert resp.json().get('booking') == body

    @allure.feature('Create booking')
    def test_create_booking_without_headers_should_be_success(self, setup):
        body: dict = {}

        with allure.step('Open booking.json'):
            with open('data/booking.json', 'r') as f:
                body = json.load(f)

        with allure.step('Create booking'):
            resp: Response = self.booking.create_booking(
                json=body,
            )

        with allure.step('Get booking id'):
            self.booking_id = resp.json().get('bookingid')

        with allure.step('Checking status code'):
            assert resp.status_code == 200, f'Incorrect status code. Got {resp.status_code}'

        with allure.step('Check booking was created with correct body'):
            assert resp.json().get('booking') == body
