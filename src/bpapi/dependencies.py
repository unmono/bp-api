from typing import Annotated
from datetime import datetime, timedelta
from jose import JWTError, ExpiredSignatureError, jwt
from passlib.context import CryptContext

from fastapi import status, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from starlette.requests import Request

import schemas
from users import users
from sqlite_um.user_manager import SQLiteUserManager

from settings import ApiSettings
settings = ApiSettings()


class CookieOAuth2(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> str | None:
        cookie_token = request.cookies.get('access_token')
        header_token = request.headers.get('Authorization')
        if header_token:
            return await super().__call__(request)
        if cookie_token:
            return cookie_token
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )


oauth2_scheme = CookieOAuth2(
    tokenUrl='/login',
    scopes={
        'user_manager': "Add or delete users",
        'catalogue': "View catalogue"
    },
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


def get_current_user(security_scopes: SecurityScopes,
                     token: Annotated[str, Depends(oauth2_scheme)]) -> schemas.User:
    authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'\
        if security_scopes.scopes\
        else 'Bearer'

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid credentials',
        headers={'WWW-Authenticate': authenticate_value}
    )
    try:
        payload = jwt.decode(token, settings.AUTH_KEY, algorithms=[settings.AUTH_ALG, ])
        if (username := payload.get('sub')) is None:
            raise credentials_exception
        token_scopes = payload.get('scopes', [])
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Credentials expired',
            headers={'WWW-Authenticate': authenticate_value}
        )
    except JWTError:
        raise credentials_exception

    token_data = schemas.TokenData(
        username=username,
        scopes=token_scopes,
    )

    if (user := get_user(token_data.username)) is None:
        raise credentials_exception

    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Not enough permissions',
                headers={'WWW-Authenticate': authenticate_value}
            )

    return schemas.User(username=user.username)
