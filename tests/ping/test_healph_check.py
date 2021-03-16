import requests


def test_health_check_should_return_success(url: str) -> None:
    resp = requests.get(url + '/ping')

    assert resp.status_code == 201
    assert resp.text == 'Created'
