from requests.models import Response
from booking_service import Booking

from jsonschema import validate


def test_get_booking_ids_should_return_booking_ids(base_url: str):
    schema: dict = {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'type': 'array',
        'properties': {
            'bookingId': {
                'type': 'number'
            }
        },
        'required': ['bookingId'],
        'maxItems': 20
    }

    resp: Response = Booking(base_url).get_booking_ids()

    assert resp.status_code == 200
    validate(resp.json(), schema)
