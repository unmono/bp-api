from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder

import dependencies
import schemas
from sqlite_um.user_manager import SQLiteUserManager, UserAlreadyExists

from settings import ApiSettings
settings = ApiSettings()


router = APIRouter(
    tags=['UM'],
    dependencies=[
        Depends(dependencies.get_current_user),
    ],
    prefix=settings.ROUTE_PREFIX + '/users',
)


def get_user_manager():
    return SQLiteUserManager(database_path='users.sqlite')


@router.get('/', response_model=list[schemas.User])
def get_user_list(um: SQLiteUserManager = Depends(get_user_manager)):
    return um.get_all_users()


router.responses = {422: {'model': list[schemas.ValidationErrorSchema]}}


@router.post('/', response_model=list[schemas.User])
def add_new_user(new_user: schemas.UserValidation,
                 um: SQLiteUserManager = Depends(get_user_manager)):
    new_user.password = dependencies.hash_password(new_user.password)
    try:
        um.add_user(**new_user.dict())
    except UserAlreadyExists as exc:
        raise HTTPException(
            status_code=422,
            detail=[jsonable_encoder(schemas.ValidationErrorSchema(
                loc='username',
                msg=str(exc)
            )), ]
        )
    else:
        return um.get_all_users()


@router.delete('/{username}', response_model=list[schemas.User])
def delete_user(username: str,
                um: SQLiteUserManager = Depends(get_user_manager)):
    poor_user = schemas.User(
        username=username
    )
    um.delete_user(poor_user.username)
    return um.get_all_users()
