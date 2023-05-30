from fastapi import APIRouter, Depends, Security
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder

import dependencies
from schemas import User, UserValidation, ValidationErrorSchema
from sqlite_um.user_manager import SQLiteUserManager, UserAlreadyExists

from settings import ApiSettings
settings = ApiSettings()


router = APIRouter(
    tags=['UM'],
    dependencies=[
        Security(dependencies.get_current_user, scopes=['user_manager']),
    ],
    prefix=settings.ROUTE_PREFIX + '/users',
)


def get_user_manager():
    return SQLiteUserManager(database_path=settings.USERS_DB_PATH)


@router.get('/', response_model=list[User])
def get_user_list(um: SQLiteUserManager = Depends(get_user_manager)):
    return um.get_all_users()


router.responses = {422: {'model': list[ValidationErrorSchema]}}


@router.post('/', response_model=list[User])
def add_new_user(new_user: UserValidation,
                 um: SQLiteUserManager = Depends(get_user_manager)):
    new_user.password = dependencies.hash_password(new_user.password)
    try:
        um.add_user(**new_user.dict())
    except UserAlreadyExists as exc:
        raise HTTPException(
            status_code=422,
            detail=[jsonable_encoder(ValidationErrorSchema(
                loc='username',
                msg=str(exc)
            )), ]
        )
    else:
        return um.get_all_users()


@router.delete('/{username}', response_model=list[User])
def delete_user(username: str,
                um: SQLiteUserManager = Depends(get_user_manager)):
    poor_user = User(
        username=username
    )
    um.delete_user(poor_user.username)
    return um.get_all_users()
