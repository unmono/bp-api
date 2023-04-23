from typing import Annotated
from datetime import timedelta

from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

import schemas
import dependencies

from settings import ApiSettings
settings = ApiSettings()

router = APIRouter(
    tags=['Auth'],
)


@router.post('/login/', response_model=schemas.Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = dependencies.authenticate_user(form_data.username, form_data.password)
    token_expire_delta = timedelta(hours=settings.TOKEN_EXPIRE_HOURS)
    token = dependencies.create_token(
        user_data={'sub': user.username, 'scopes': form_data.scopes},
        expires_delta=token_expire_delta,
    )
    return schemas.Token(access_token=token, token_type='bearer')
