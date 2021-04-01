from booking_service import BookingPing
from requests.models import Response


def test_health_check_should_return_success(base_url: str) -> None:
    resp: Response = BookingPing(base_url).ping()

    assert resp.status_code == 201
    assert resp.text == 'Created'
