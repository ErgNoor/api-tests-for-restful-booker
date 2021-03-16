from booking_service import Booking

from jsonschema import validate

import pytest


class TestBookingAuth:
    @pytest.fixture
    def setup(self, base_url):
        self.booking = Booking(base_url)
        yield

    @pytest.mark.parametrize('booking_id', [1, 2, 3, 4, 5])
    def test_get_booking_should_return_booking(self, setup, booking_id):
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

        resp = self.booking.get_booking(booking_id, headers={'Accept': 'application/json'})

        assert resp.status_code == 200
        validate(resp.json(), schema)

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

        resp = self.booking.get_booking(5)

        assert resp.status_code == 200
        validate(resp.json(), schema)

    def test_get_non_exist_booking_should_be_failed(self, setup):
        
        resp = self.booking.get_booking(booking_id=-1, headers={'Accept': 'application/json'})

        assert resp.status_code == 404, 'Non-exist booking was found'
        assert resp.text == 'Not Found'