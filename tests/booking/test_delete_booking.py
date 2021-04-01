from booking_service import Booking, BookingAuth

import pytest
import allure

import json
from requests.models import Response

import logging


logging.basicConfig(
    level=logging.INFO,
)
delete_booking_logger = logging.getLogger(__name__)


class TestDeleteBooking:
    @pytest.fixture
    def setup(self, base_url: str, pytestconfig):
        self.url: str = base_url
        self.booking: Booking = Booking(base_url)
        username: str = pytestconfig.getoption('username')
        password: str = pytestconfig.getoption('password')
        self.creds: dict = {'username': username, 'password': password}

        body: dict = {}

        with allure.step('Open booking.json'):
            with open('data/booking.json', 'r') as f:
                body = json.load(f)

        with allure.step('Create booking'):
            create_resp: Response = self.booking.create_booking(
                json=body,
                headers={
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            )

        with allure.step('Get created booking id'):
            self.booking_id: int = create_resp.json().get('bookingid')
            delete_booking_logger.info(f'{self.booking_id =}')

        with allure.step('Check status code for create booking'):
            if create_resp.status_code == 200:
                delete_booking_logger.info(f'booking with {self.booking_id=} was created successful')
            else:
                delete_booking_logger.info(f'booking with {self.booking_id=} was not created')

        yield

    def test_delete_booking_without_authorisation_should_be_fail(self, setup):
        with allure.step('Delete booking'):
            resp: Response = self.booking.delete_booking(self.booking_id)
        
        with allure.step('Check status code'):
            assert resp.status_code == 403, f'Incorrect status code. Got {resp.status_code}'


    def test_delete_booking_with_cookie_auth_should_be_success(self, setup):
        with allure.step('Get token'):
            token: str = BookingAuth(self.url).auth(json=self.creds, headers={'Content-Type': 'application/json'}).json().get('token')
            delete_booking_logger.info(f'{token=}')

        with allure.step('Delete booking'):
            resp: Response = self.booking.delete_booking(
                self.booking_id,
                headers =
                {
                    'Content-Type': 'application/json',
                    'Cookie': f'token={token}'
                }
            )
        
        with allure.step('Check status code'):
            assert resp.status_code == 201, f'Incorrect status code. Got {resp.status_code}'


    @pytest.mark.xfail(reason='Basic auth not implemented')
    def test_delete_booking_with_basic_auth_should_be_success(self, setup):
        # token_id: str = BookingAuth(self.url).auth(json=self.creds, headers={'Content-Type': 'application/json'}).json().get('token')
        # print(token_id)
        
        # resp = self.booking.delete_booking(
        #     self.booking_id,
        #     headers =
        #     {
        #         'Content-Type': 'application/json',
        #         'Authorisation': f'Basic {token_id}'
        #     }
        # )
        
        # assert resp.status_code == 200, f'Incorrect status code. Got {resp.status_code}'
        pass
