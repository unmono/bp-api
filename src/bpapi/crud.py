from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload, selectinload

from models import (
    Subsub,
    Section,
    SubSection,
    PartNumber,
    Product
)


def get_all_subs(db: Session):
    # These run multiple queries:
    # return db.query(Section).all()
    # return db.query(Subsub.title, ).\
    #     join(SubSection).join(Section).all()

    # This one runs one query but returns redundant data
    return db.query(Subsub.id.label('url'),
                    Subsub.title.label('title'),
                    SubSection.title.label('subsection'),
                    Section.title.label('section')).\
        select_from(Subsub).join(SubSection).join(Section).all()


def get_products_by_subsub(db: Session, subsub_id: int):
    return db.query(PartNumber.part_no, Product.title_en).\
        select_from(Product).\
        join(PartNumber).\
        filter(Product.subsub_id == subsub_id).all()


def get_partnum(db: Session, part_no: str):
    stmt = select(PartNumber)\
        .options(joinedload(PartNumber.product),
                 joinedload(PartNumber.masterdata),
                 selectinload(PartNumber.refers))\
        .where(PartNumber.part_no == part_no)

    return db.execute(stmt).scalar()


def search_products(db: Session, query):
    stmt = select(PartNumber.part_no).where(PartNumber.part_no.like(query))
    return db.execute(stmt).all()
