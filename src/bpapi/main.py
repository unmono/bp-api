import re
from datetime import timedelta, datetime
from collections import defaultdict
from typing import Annotated
from jose import JWTError, jwt
from passlib.context import CryptContext

from fastapi import Depends, Path, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.security import (
    OAuth2PasswordRequestForm,
    OAuth2PasswordBearer
)

from sqlalchemy.orm import Session
# import databases - asyncio support for databases. Doesn't support sqlalchemy2.

from app import app
import schemas
import crud
from database import db_session
from users import users

from settings import ApiSettings
settings = ApiSettings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/login')
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_user(username,
             stored_users: dict[str: dict] = users) -> schemas.UserValidation | None:
    return schemas.UserValidation(**stored_users[username]) \
        if username in stored_users \
        else None


def authenticate_user(username: str,
                      password: str) -> schemas.UserValidation:
    """

    :param username:
    :param password:
    :return:
    """
    if (user := get_user(username)) is not None:
        if pwd_context.verify(password, user.hashed_password):
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
        if username := payload.get('sub') is None:
            raise credentials_exception
        if user := get_user(username) is None:
            raise credentials_exception
    # ExpiredSignatureError - subclass of JWTError
    except JWTError:
        raise credentials_exception
    return user


@app.exception_handler(RequestValidationError)
async def validation_exception(request, exc: RequestValidationError) -> JSONResponse:
    error_messages = [schemas.ValidationErrorSchema(
        loc=err['loc'][-1],
        msg=err['msg'].capitalize(),
    ) for err in exc.errors()]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({'detail': error_messages})
    )


LoggedUserDependency = Annotated[schemas.User, Depends(get_current_user)]


@app.get('/sections/',
         tags=['Sections'],
         response_model=list[schemas.Section])
async def sections(user: LoggedUserDependency,
                   db: Session = Depends(db_session)):
    """
    Complete list of sections, subsections and group in current Bosch price.
    """

    # [(pk, title, subsection, section), ...]
    fetched_list_of_groups = crud.get_all_groups(db)

    # {section1: {subsection1: [sub_subsection1, ...], ...}, ...}
    dict_of_sections = defaultdict(lambda: defaultdict(list))

    for pk, title, subsection, section in fetched_list_of_groups:
        group = {
            'id': pk,
            'title': title,
        }
        dict_of_sections[section][subsection].append(group)

    # If models are defined, the instances are created twice as well as validation's run.
    return [{'title': section, 'subsections': [
        {'title': subsection, 'subsections': groups_list}
        for subsection, groups_list in subsection_dict.items()
    ]} for section, subsection_dict in dict_of_sections.items()]


# Thus it won't be in sections openapi docs
app.router.responses = {422: {'model': list[schemas.ValidationErrorSchema]}}


@app.get('/sections/{group_id}/',
         tags=['Products'])
async def products_by_group(user: LoggedUserDependency,
                            group_id: int = Path(title='The ID of group of products.', ge=1),
                            db: Session = Depends(db_session)) -> list[schemas.ListedPartnums]:
    """
    List of products in selected calatogue group.
    """

    list_of_products = crud.get_products_by_group(db, group_id)
    return list_of_products


@app.get('/products/{part_number}/',
         tags=['Products'],
         response_model=schemas.PartNumber)
async def product(user: LoggedUserDependency,
                  part_number: str, db: Session = Depends(db_session)):
    """
    Detail catalogue info for the requested product.
    """
    if not re.fullmatch(r'[a-zA-Z0-9]{10}', part_number):
        raise HTTPException(
            status_code=422,
            detail=[jsonable_encoder(schemas.ValidationErrorSchema(
                loc='part_number',
                msg='Enter a valid Bosch part number'
            )), ]
        )

    p = crud.get_partnum(db, part_no=part_number.upper())
    if not p:
        raise HTTPException(status_code=404, detail='No such product')
    return p


@app.post('/products/search/',
          tags=['Products'],
          response_model=list[schemas.ListedPartnums])
async def search(user: LoggedUserDependency,
                 search_request: schemas.SearchRequest,
                 db: Session = Depends(db_session)):
    """
    Search for specific part number in Bosch catalogue.
    """
    results = crud.search_products(db, search_request.search_query)
    return results


@app.post('/login/', tags=['Auth'], response_model=schemas.Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password)
    token_expire_delta = timedelta(hours=settings.TOKEN_EXPIRE_HOURS)
    token = create_token(
        user_data={'sub': user.username},
        expires_delta=token_expire_delta,
    )
    return schemas.Token(access_token=token, token_type='bearer')
