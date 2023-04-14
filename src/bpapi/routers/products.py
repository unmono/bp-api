import re
from typing import Annotated
from collections import defaultdict

from fastapi import Depends, APIRouter, Path
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

import schemas
import crud
import database
import dependencies

from settings import ApiSettings
settings = ApiSettings()


LoggedUserDependency = Annotated[schemas.User, Depends(dependencies.get_current_user)]

router = APIRouter(
    tags=['Catalogue'],
    dependencies=[Depends(dependencies.get_current_user)],
    prefix=settings.ROUTE_PREFIX
)


@router.get('/sections/', response_model=list[schemas.Section])
async def sections(user: LoggedUserDependency,
                   db: Session = Depends(database.db_session)):
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
router.responses = {422: {'model': list[schemas.ValidationErrorSchema]}}


@router.get('/sections/{group_id}/')
async def products_by_group(user: LoggedUserDependency,
                            group_id: int = Path(title='The ID of group of products.', ge=1),
                            db: Session = Depends(database.db_session)) -> list[schemas.ListedPartnums]:
    """
    List of products in selected calatogue group.
    """

    list_of_products = crud.get_products_by_group(db, group_id)
    return list_of_products


@router.get('/products/{part_number}/', response_model=schemas.PartNumber)
async def product(user: LoggedUserDependency,
                  part_number: str, db: Session = Depends(database.db_session)):
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


@router.post('/products/search/', response_model=list[schemas.ListedPartnums])
async def search(user: LoggedUserDependency,
                 search_request: schemas.SearchRequest,
                 db: Session = Depends(database.db_session)):
    """
    Search for specific part number in Bosch catalogue.
    """
    results = crud.search_products(db, search_request.search_query)
    return results
