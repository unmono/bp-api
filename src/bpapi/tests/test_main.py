from datetime import timedelta
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


@pytest.fixture
def stored_users():
    hashed_test_password = dependencies.pwd_context.hash('hashed_test_password')

    return {
        'test_user': {
            'username': 'test_user',
            'hashed_password': 'hashed_test_password'
        },
        'user_hashed_password': {
            'username': 'user_hashed_password',
            'hashed_password': hashed_test_password
        }
    }


def test_get_user(stored_users):
    user = dependencies.get_user('test_user', stored_users=stored_users)
    assert user is not None
    assert user.dict() == stored_users['test_user']


def test_authenticate_user(stored_users):
    try:
        user = dependencies.authenticate_user(
            username='user_hashed_password',
            password='hashed_test_password',
            stored_users=stored_users
        )
    except HTTPException as exc:
        assert False, exc.detail

    assert user.dict() == stored_users['user_hashed_password']


def test_create_token():
    tkn = dependencies.create_token(
        user_data={'sub': 'user_hashed_password'},
        expires_delta=timedelta(hours=1),
    )
    payload = jwt.decode(tkn, settings.AUTH_KEY, algorithms=[settings.AUTH_ALG, ])
    assert payload.get('sub') == 'user_hashed_password'


def test_get_current_user(monkeypatch, stored_users):
    tkn = dependencies.create_token(
        user_data={'sub': 'user_hashed_password'},
        expires_delta=timedelta(hours=1),
    )
    monkeypatch.setitem(dependencies.users, 'user_hashed_password', stored_users['user_hashed_password'])
    user = dependencies.get_current_user(tkn)
    assert user.dict() == {'username': 'user_hashed_password'}


def test_get_current_user_expired(monkeypatch, stored_users):
    tkn = dependencies.create_token(
        user_data={'sub': 'user_hashed_password'},
        expires_delta=timedelta(hours=-1),
    )
    monkeypatch.setitem(dependencies.users, 'user_hashed_password', stored_users['user_hashed_password'])
    with pytest.raises(HTTPException):
        dependencies.get_current_user(tkn)


def test_get_current_user_wrong(monkeypatch, stored_users):
    tkn = dependencies.create_token(
        user_data={'sub': 'wrong_username'},
        expires_delta=timedelta(hours=1),
    )
    monkeypatch.setitem(dependencies.users, 'user_hashed_password', stored_users['user_hashed_password'])
    with pytest.raises(HTTPException):
        dependencies.get_current_user(tkn)


def test_get_current_user_compromized_token(monkeypatch, stored_users):
    tkn = dependencies.create_token(
        user_data={'sub': 'user_hashed_password'},
        expires_delta=timedelta(hours=1),
    )
    tkn_parts = tkn.split('.')
    tkn_parts[1] = tkn_parts[1][::-1]
    compromized_token = '.'.join(tkn_parts)
    monkeypatch.setitem(dependencies.users, 'user_hashed_password', stored_users['user_hashed_password'])
    with pytest.raises(HTTPException):
        dependencies.get_current_user(compromized_token)


def test_login(monkeypatch, stored_users):
    user = stored_users['user_hashed_password']
    monkeypatch.setitem(dependencies.users, user['username'], user)
    response = client.post(
        url='/login/',
        headers={
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        data={
            'username': 'user_hashed_password',
            'password': 'hashed_test_password',
        }
    )
    assert response.status_code == 200
    authenticated_user = dependencies.get_current_user(response.json()['access_token'])
    assert authenticated_user.username == user['username']


@pytest.fixture
def access_token(monkeypatch, stored_users):
    monkeypatch.setitem(dependencies.users, 'user_hashed_password', stored_users['user_hashed_password'])
    response = client.post(
        url='/login/',
        headers={
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        data={
            'username': 'user_hashed_password',
            'password': 'hashed_test_password',
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
def test_sections(access_token, monkeypatch, stored_users, url):
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
