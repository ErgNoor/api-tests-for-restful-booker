from requests.models import Response
from booking_service import Booking

from jsonschema import validate
from jsonschema.exceptions import ValidationError

import pytest


class TestGetBooking:
    @pytest.fixture
    def setup(self, base_url: str):
        self.booking = Booking(base_url)
        yield

    @pytest.mark.parametrize('booking_id', [1, 2, 3, 4, 5])
    def test_get_booking_should_return_booking(self, setup, booking_id: int):
        schema = {
            '$schema': 'http://json-schema.org/draft-04/schema#',
            'type': 'object',
            'properties': {
                'firstname': {
                    'type': 'string'
                },
                'lastname': {
                    'type': 'string'
                },
                'totalprice':{
                    'type': 'number'
                },
                'depositpaid':{
                    'type': 'boolean'
                },
                'bookingdates': {
                    'checkin':{
                        'type': 'string'
                    },
                    'checkout':{
                        'type': 'string'
                    },
                },
                'additionalneeds': {
                    'type': 'string'
                }
            },
            'required': [
                'firstname',
                'lastname',
                'totalprice',
                'depositpaid',
                'bookingdates',
                'additionalneeds'
            ]
        }

        resp: Response= self.booking.get_booking(booking_id, headers={'Accept': 'application/json'})

        assert resp.status_code == 200
        try:
            validate(resp.json(), schema)
        except ValidationError as e:
            assert False, e.message

    def test_get_booking_without_headers_should_return_booking(self, setup):
        schema = {
            '$schema': 'http://json-schema.org/draft-04/schema#',
            'type': 'object',
            'properties': {
                'firstname': {
                    'type': 'string'
                },
                'lastname': {
                    'type': 'string'
                },
                'totalprice':{
                    'type': 'number'
                },
                'depositpaid':{
                    'type': 'boolean'
                },
                'bookingdates': {
                    'checkin':{
                        'type': 'string'
                    },
                    'checkout':{
                        'type': 'string'
                    },
                },
                'additionalneeds': {
                    'type': 'string'
                }
            },
            'required': [
                'firstname',
                'lastname',
                'totalprice',
                'depositpaid',
                'bookingdates',
                'additionalneeds'
            ]
        }

        resp: Response = self.booking.get_booking(5)

        assert resp.status_code == 200
        try:
            validate(resp.json(), schema)
        except ValidationError as e:
            assert False, e.message

    def test_get_non_exist_booking_should_be_failed(self, setup):
        
        resp: Response = self.booking.get_booking(booking_id=-1, headers={'Accept': 'application/json'})

        assert resp.status_code == 404, 'Non-exist booking was found'
        assert resp.text == 'Not Found'
