import pytest


def pytest_addoption(parser):
    parser.addoption('--url', action='store', default=None)
    parser.addoption('--username', action='store', default = None)
    parser.addoption('--password', action='store', default = None)


@pytest.fixture(scope='class')
def base_url(request):
    url = request.config.getoption('url')
    return url or 'https://restful-booker.herokuapp.com/'


@pytest.fixture
def credentials(request):
    # admin password123
    username = request.config.getoption('username')
    password = request.config.getoption('password')
    return {'username': username or 'admin', 'password': password or 'password123'}


