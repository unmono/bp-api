from datetime import timedelta
from dataclasses import dataclass
import pytest
import sys
sys.path.insert(0, './')

from jose import jwt, JWTError, ExpiredSignatureError
from fastapi.testclient import TestClient
from fastapi.exceptions import HTTPException

from ..main import app
from .. import dependencies
from .. import schemas
from .. import settings

settings = settings.ApiSettings()

client = TestClient(app)


@dataclass
class SetupUser:
    username: str
    password: str
    # hashed_password: str

    @property
    def hashed_password(self) -> str:
        return dependencies.pwd_context.hash(self.password)


@pytest.fixture
def test_user(monkeypatch) -> SetupUser:
    test_user = SetupUser(
        username='user_hashed_password',
        password='hashed_test_password',
        # hashed_password='$2b$12$dUkM5ijvyw6xs7iBRGxGy.5gaAE6HpT2tHLdKDmT1z5ABEjskPit6',
    )
    monkeypatch.setitem(
        dependencies.users,
        test_user.username,
        {'username': test_user.username, 'hashed_password': test_user.hashed_password},
    )
    yield test_user


def test_get_user(test_user):
    user = dependencies.get_user(test_user.username)
    assert user is not None
    assert user.username == test_user.username


def test_get_wrong_user(test_user):
    user = dependencies.get_user('wrong_username')
    assert user is None


def test_authenticate_user(test_user):
    try:
        user = dependencies.authenticate_user(
            username=test_user.username,
            password=test_user.password,
        )
    except HTTPException as exc:
        assert False, exc.detail

    assert user.username == test_user.username


def test_authenticate_user_fail(test_user):
    with pytest.raises(HTTPException):
        user = dependencies.authenticate_user(
            username=test_user.username,
            password='wrong_password',
        )


def test_create_token(test_user):
    tkn = dependencies.create_token(
        user_data={'sub': test_user.username},
        expires_delta=timedelta(hours=1),
    )
    payload = jwt.decode(tkn, settings.AUTH_KEY, algorithms=[settings.AUTH_ALG, ])
    assert payload.get('sub') == test_user.username


def test_get_current_user(test_user):
    tkn = dependencies.create_token(
        user_data={'sub': test_user.username},
        expires_delta=timedelta(hours=1),
    )
    user = dependencies.get_current_user(tkn)
    assert user.dict() == {'username': test_user.username}


def test_get_current_user_expired(test_user):
    tkn = dependencies.create_token(
        user_data={'sub': test_user.username},
        expires_delta=timedelta(hours=-1),
    )
    with pytest.raises(HTTPException):
        dependencies.get_current_user(tkn)


def test_get_current_user_wrong(test_user):
    tkn = dependencies.create_token(
        user_data={'sub': 'wrong_username'},
        expires_delta=timedelta(hours=1),
    )
    with pytest.raises(HTTPException):
        dependencies.get_current_user(tkn)


def test_get_current_user_compromized_token(test_user):
    tkn = dependencies.create_token(
        user_data={'sub': test_user.username},
        expires_delta=timedelta(hours=1),
    )
    tkn_parts = tkn.split('.')
    tkn_parts[1] = tkn_parts[1][::-1]
    compromized_token = '.'.join(tkn_parts)
    with pytest.raises(HTTPException):
        dependencies.get_current_user(compromized_token)


def test_login(test_user):
    response = client.post(
        url='/login/',
        headers={
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        data={
            'username': test_user.username,
            'password': test_user.password,
        }
    )
    assert response.status_code == 200
    authenticated_user = dependencies.get_current_user(response.json()['access_token'])
    assert authenticated_user.username == test_user.username


@pytest.fixture
def access_token(test_user):
    response = client.post(
        url='/login/',
        headers={
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        data={
            'username': test_user.username,
            'password': test_user.password,
        }
    )
    return response.json()['access_token']


get_urls_list = [
    '/api/v1/sections/',
    '/api/v1/sections/12/',
    '/api/v1/products/0445115007',
]


@pytest.mark.parametrize(
    'url',
    get_urls_list
)
def test_sections(access_token, url):
    response = client.get(
        url,
        headers={
            'Authorization': f'Bearer {access_token}'
        }
    )
    assert response.status_code == 200


@pytest.mark.parametrize(
    'url',
    get_urls_list
)
def test_no_token_get_endpoints(url):
    response = client.get(url)
    assert response.status_code == 401, url
    assert response.json() == {'detail': 'Not authenticated'}, url


@pytest.mark.parametrize(
    'url',
    [
        '/api/v1/sections/0/',
        '/api/v1/sections/a/',
        '/api/v1/sections/True/',
        '/api/v1/products/04451150071',
        '/api/v1/products/044511500',
        '/api/v1/products/44?5111500',
        '/api/v1/products/0445115_07',
        '/api/v1/products/F00VC175!3',
    ]
)
def test_get_validation_errors(url, access_token):
    response = client.get(
        url,
        headers={
            'Authorization': f'Bearer {access_token}'
        }
    )
    assert response.status_code == 422, url
