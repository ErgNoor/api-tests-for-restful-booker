import requests

from requests.models import Response

from typing import Optional


class BookingAuth():
    def __init__(self, base_url) -> None:
        super().__init__()
        self.base_url = base_url + 'auth'
        

    def auth(self, params=None, data=None, json=None, headers=None) -> Response:
        return requests.post(url=self.base_url, params=params, data=data, json=json, headers=headers)


class Booking:
    def __init__(self, base_url: str, creds: Optional[dict] = None) -> None:
        super().__init__()
        self.booking_url = base_url + 'booking/'
        self.creds = creds

    def get_booking_ids(self, path="/", params=None, headers=None) -> Response:
        
        resp = requests.get(self.booking_url, params=params, headers=headers)

        return resp

    def get_booking(self, booking_id: int, headers=None) -> Response:
        resp = requests.get(self.booking_url + str(booking_id), headers=headers)

        return resp

    def create_booking(self, params=None, data=None, json: Optional[dict] = None, headers: Optional[dict] = None) -> Response:
        return requests.post(self.booking_url, params=params, data=data, json=json, headers=headers)

    def update_booking(self, booking_id: int, json: Optional[dict] = None, headers: Optional[dict] = None):
        return requests.put(self.booking_url + str(booking_id), json=json, headers=headers)

    def partial_update_booking(self, booking_id: int, json: Optional[dict] = None, headers: Optional[dict] = None):
        return requests.patch(self.booking_url + str(booking_id), json=json, headers=headers)

    def delete_booking(self, booking_id: int, headers: Optional[dict] = None) -> Response:
        resp = requests.delete(self.booking_url + str(booking_id), headers=headers)

        return resp


class BookingPing:
    def __init__(self, url: str) -> None:
        super().__init__()
        self.url = url + 'ping'

    def ping(self) -> Response:
        return requests.get(self.url)
