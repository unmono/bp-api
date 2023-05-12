from typing import Annotated
from datetime import timedelta

from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from schemas import Token
from dependencies import authenticate_user, create_token

from settings import ApiSettings
settings = ApiSettings()

router = APIRouter(
    tags=['Auth'],
)


@router.post('/api/v1/login/', response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password)
    token_expire_delta = timedelta(hours=settings.TOKEN_EXPIRE_HOURS)
    token = create_token(
        user_data={'sub': user.username, 'scopes': user.scopes},
        expires_delta=token_expire_delta,
    )
    return Token(access_token=token, token_type='bearer')
