from typing import Annotated
from datetime import datetime, timedelta
from jose import JWTError, ExpiredSignatureError, jwt
from passlib.context import CryptContext

from fastapi import status, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer

import schemas
from users import users
from sqlite_um.user_manager import SQLiteUserManager

from settings import ApiSettings
settings = ApiSettings()


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='/login',
    # scopes={
    #     'user_manager': "Add or delete users.",
    #     'catalogue': "View catalogue."
    # }
)
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_user(username,
             stored_users: dict[str: dict] | SQLiteUserManager = users) -> schemas.UserValidation | None:
    """

    :param username:
    :param stored_users:
    :return:
    """
    return schemas.UserValidation(**stored_users[username]) \
        if username in stored_users \
        else None


def hash_password(unhashed: str):
    return pwd_context.hash(unhashed)


def authenticate_user(username: str,
                      password: str,
                      stored_users: dict[str: dict] = users) -> schemas.UserValidation:
    """

    :param username:
    :param password:
    :param stored_users:
    :return:
    """
    if (user := get_user(username, stored_users)) is not None:
        if pwd_context.verify(password, user.password):
            return user
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Incorrect username or password'
    )


def create_token(user_data: dict, expires_delta: timedelta = timedelta(hours=1)):
    """

    :param user_data:
    :param expires_delta:
    :return:
    """
    data_to_encode = user_data.copy()
    expire = datetime.utcnow() + expires_delta
    data_to_encode.update({'exp': expire})
    return jwt.encode(data_to_encode, settings.AUTH_KEY, algorithm=settings.AUTH_ALG)


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> schemas.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    try:
        payload = jwt.decode(token, settings.AUTH_KEY, algorithms=[settings.AUTH_ALG, ])
        if (username := payload.get('sub')) is None:
            raise credentials_exception
        if (user := get_user(username)) is None:
            raise credentials_exception
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Credentials expired',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    except JWTError:
        raise credentials_exception
    return schemas.User(username=user.username)
