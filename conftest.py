import pytest


@pytest.fixture
def url():
    return 'https://restful-booker.herokuapp.com'


@pytest.fixture
def credentials():
    return {'username': 'admin', 'password': 'password123'}
