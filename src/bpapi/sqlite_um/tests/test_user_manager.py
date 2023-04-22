import pytest
import sqlite3
import os
from ..user_manager import SQLiteUserManager, UserAlreadyExists, UserDoesNotExist


EXAMPLE_USER = {
    'username': 'example_user',
    'password': 'password',
    'scopes': ['scope1', 'scope2']
}


SUPPORTED_TABLE_SCHEMAS = [
    {
        'username': 'TEXT',
        'password': 'TEXT',
        'scopes': 'TEXT',
    },
    {},
]

UNSUPPORTED_TABLE_SCHEMAS = [
    {
        'username': 'TEXT',
        'scopes': 'TEXT',
    },
    {
        'username': 'TEXT',
        'password': 'TEXT',
        'scopes': 'TEXT',
        'not_expected': 'TEXT',
    },
]


@pytest.fixture(params=SUPPORTED_TABLE_SCHEMAS)
def given_db(request):
    db_name = 'normal.sqlite'
    if request.param:
        conn = sqlite3.connect(db_name)
        conn.execute(f"""
            CREATE TABLE users ({','.join([f'{k} {v}' for k, v in request.param.items()])})
        """)
        conn.close()
    yield SQLiteUserManager(db_name)
    os.remove(db_name)


@pytest.fixture
def setted_up_db(given_db):
    given_db._initial_setup()
    return given_db


def test_initial_setup(given_db):
    try:
        given_db._initial_setup()
    except AssertionError as e:
        assert False, repr(e)


@pytest.mark.parametrize('given_db', UNSUPPORTED_TABLE_SCHEMAS, indirect=True)
def test_initial_setup_unsupported_db(given_db):
    with pytest.raises(AssertionError):
        given_db._initial_setup()


def test_add_user(setted_up_db):
    assert EXAMPLE_USER['username'] not in setted_up_db
    setted_up_db.add_user(**EXAMPLE_USER)
    with setted_up_db._db_connection() as db:
        just_added_user = db.execute(
            'SELECT COUNT(*) FROM users WHERE username = ?;',
            (EXAMPLE_USER['username'], )
        ).fetchone()

    assert just_added_user[0] == 1


def test_add_existed_user(setted_up_db):
    setted_up_db.add_user(**EXAMPLE_USER)
    with pytest.raises(UserAlreadyExists):
        setted_up_db.add_user(**EXAMPLE_USER)


def test_delete_user(setted_up_db):
    setted_up_db.add_user(**EXAMPLE_USER)
    setted_up_db.delete_user(EXAMPLE_USER['username'])
    with setted_up_db._db_connection() as db:
        just_added_user = db.execute(
            'SELECT COUNT(*) FROM users WHERE username = ?;',
            (EXAMPLE_USER['username'], ),
        ).fetchone()

    assert just_added_user[0] == 0


def test_get_user_dict(setted_up_db):
    setted_up_db.add_user(**EXAMPLE_USER)
    user_dict = setted_up_db.get_user_dict(EXAMPLE_USER['username'])

    assert user_dict == EXAMPLE_USER


def test_get_not_existed_user_dict(setted_up_db):
    setted_up_db.add_user(**EXAMPLE_USER)
    with pytest.raises(UserDoesNotExist):
        user_dict = setted_up_db.get_user_dict('not_existed_username')


def test_get_user_list(setted_up_db):
    setted_up_db.add_user(**EXAMPLE_USER)
    setted_up_db.add_user(**{
        'username': 'example_user2',
        'password': 'password',
        'scopes': ['scope1', 'scope2']
    })
    setted_up_db.add_user(**{
        'username': 'example_user3',
        'password': 'password',
        'scopes': ['scope1', 'scope2']
    })
    user_list = setted_up_db.get_all_users()
    assert len(user_list) == 3
    assert user_list == [
        {'username': EXAMPLE_USER['username']},
        {'username': 'example_user2'},
        {'username': 'example_user3'},
    ]
