from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
# import databases - asyncio support for databases

import database
import schemas
import models
import crud as jr

# from . import (
#     database,
#     schemas,
#     models,
#     crud as jr,
# ) ...although, if it's not unique, or your package structure is more complex,
# you'll need to include the directory containing your package directory in
# PYTHONPATH, and do it like this... from stackoverflow

app = FastAPI()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/sections', response_model=dict[str, dict[str, list[schemas.Subsub]]])
def sections(db: Session = Depends(get_db)) -> dict[str, dict[str, list]]:
    list_of_subs = jr.get_all_subs(db)
    dict_of_sections = {}
    for pk, title, subsection, section in list_of_subs:
        subsub_data = {
            'url': app.url_path_for('products_by_subsub', subsub_id=pk),
            'title': title,
        }
        subsection_dict = dict_of_sections.setdefault(section, {})
        list_of_subsubsections = subsection_dict.setdefault(subsection, [])
        list_of_subsubsections.append(subsub_data)
    return dict_of_sections


@app.get('/sections/{subsub_id}', response_model=list[schemas.ListedPartnums], )
def products_by_subsub(subsub_id: int, db: Session = Depends(get_db)):
    list_of_products = jr.get_products_by_subsub(db, subsub_id)
    return list_of_products


@app.get('/products/{part_number}', response_model=schemas.PartNumber)
def product(part_number: str, db: Session = Depends(get_db)):
    p = jr.get_partnum(db, part_no=part_number)
    if not p:
        raise HTTPException(status_code=404, detail='Product nof found.')
    return p


@app.post('/search/', response_model=list[schemas.ListedPartnums])
async def search(search_request: schemas.SearchRequest, db: Session = Depends(get_db)):
    query = search_request.search_query
    results = jr.search_products(db, query)
    return results
