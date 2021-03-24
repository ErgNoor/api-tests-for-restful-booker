from booking_service import BookingPing


def test_health_check_should_return_success(base_url: str) -> None:
    resp = BookingPing(base_url).ping()

    assert resp.status_code == 201
    assert resp.text == 'Created'
