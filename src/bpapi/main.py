from collections import defaultdict
from typing import Annotated, Any
from fastapi import Depends, HTTPException, Path
from sqlalchemy.orm import Session
# import databases - asyncio support for databases

from app import app
import schemas
import crud
from database import db_session

from settings import ApiSettings
settings = ApiSettings()


@app.get('/sections',
         tags=['Sections'],
         response_model=list[schemas.Section])
async def sections(db: Session = Depends(db_session)) -> list[Any]:
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

    return [{'title': section, 'subsections': [
        {'title': subsection, 'subsections': groups_list}
        for subsection, groups_list in subsection_dict.items()
    ]} for section, subsection_dict in dict_of_sections.items()]


@app.get('/sections/{group_id}',
         tags=['Products'],
         response_model=list[schemas.ListedPartnums])
async def products_by_group(group_id: int = Path(title='The ID of group of products.', ge=0),
                            db: Session = Depends(db_session)):
    list_of_products = crud.get_products_by_group(db, group_id)
    return list_of_products


@app.get('/products/{part_number}',
         tags=['Products'],
         response_model=schemas.PartNumber)
async def product(part_number: str = Path(title='Valid Bosch part number.', regex=r'^[a-zA-Z0-9]{10}$'),
                  db: Session = Depends(db_session)):
    p = crud.get_partnum(db, part_no=part_number.upper())
    if not p:
        raise HTTPException(status_code=404, detail='No such product')
    return p


@app.post('/products/search',
          tags=['Products'],
          response_model=list[schemas.ListedPartnums])
async def search(search_request: schemas.SearchRequest, db: Session = Depends(db_session)):
    query = search_request.search_query
    results = crud.search_products(db, query)
    return results


# todo:
#  - Status codes
#  - host path
