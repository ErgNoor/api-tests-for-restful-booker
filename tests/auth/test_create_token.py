import requests

headers = {'Content-Type': 'application/json'}


def test_token_should_be_created_success(url: str, credentials: dict) -> None:
    resp = requests.post(url + '/auth', json=credentials, headers=headers)
    can_resp = eval(resp.text)

    assert resp.status_code == 200
    assert isinstance(can_resp, dict)
    assert 'token' in can_resp.keys()


def test_token_request_without_credentials_should_fail(url: str) -> None:
    resp = requests.post(url + '/auth', headers=headers)
    can_resp = eval(resp.text)

    assert resp.status_code == 200
    assert can_resp['reason'] == 'Bad credentials'


def test_token_request_without_headers_and_credentials_should_fail(url: str) -> None:
    resp = requests.post(url + '/auth')
    can_resp = eval(resp.text)

    assert resp.status_code == 200
    assert can_resp['reason'] == 'Bad credentials'
