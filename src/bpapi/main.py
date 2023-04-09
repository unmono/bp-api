import re
from collections import defaultdict
from typing import Annotated, Any

from fastapi import Depends, Path, status
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException, RequestValidationError
from starlette.exceptions import HTTPException as StartletteHTTPException
from fastapi.exception_handlers import http_exception_handler

from sqlalchemy.orm import Session
# import databases - asyncio support for databases

from app import app
import schemas
import crud
from database import db_session

from settings import ApiSettings
settings = ApiSettings()


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


@app.get('/sections',
         tags=['Sections'],
         response_model=list[schemas.Section])
async def sections(db: Session = Depends(db_session)):
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


@app.get('/sections/{group_id}',
         tags=['Products'])
async def products_by_group(group_id: int = Path(title='The ID of group of products.', ge=1),
                            db: Session = Depends(db_session)) -> list[schemas.ListedPartnums]:
    """
    List of products in selected calatogue group.
    """

    list_of_products = crud.get_products_by_group(db, group_id)
    return list_of_products


@app.get('/products/{part_number}',
         tags=['Products'],
         response_model=schemas.PartNumber)
async def product(part_number: str, db: Session = Depends(db_session)):
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


@app.post('/products/search',
          tags=['Products'],
          response_model=list[schemas.ListedPartnums])
async def search(search_request: schemas.SearchRequest, db: Session = Depends(db_session)):
    """
    Search for specific part number in Bosch catalogue.
    """
    results = crud.search_products(db, search_request.search_query)
    return results


# todo:
#  - host path
#  - async db
