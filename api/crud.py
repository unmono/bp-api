from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload, selectinload

from models import (
    Group,
    Section,
    SubSection,
    PartNumber,
    Product
)


def get_all_groups(db: Session):
    # These run multiple queries:
    # return db.query(Section).all()
    # return db.query(Subsub.title, ).\
    #     join(SubSection).join(Section).all()

    # This one fires single query but returns redundant data
    return db.query(Group.id.label('id'),
                    Group.title.label('title'),
                    SubSection.title.label('subsection'),
                    Section.title.label('section')).\
        select_from(Group).join(SubSection).join(Section).all()


def get_products_by_group(db: Session, group_id: int):
    return db.query(PartNumber.part_no, Product.title_en).\
        select_from(Product).\
        join(PartNumber).\
        filter(Product.subsub_id == group_id).all()


def get_partnum(db: Session, part_no: str):
    stmt = select(PartNumber)\
        .options(joinedload(PartNumber.product),
                 joinedload(PartNumber.masterdata),
                 selectinload(PartNumber.refers))\
        .where(PartNumber.part_no == part_no)

    return db.execute(stmt).scalar()


def search_products(db: Session, query):
    stmt = select(PartNumber.part_no, Product.title_en).\
        join(Product, isouter=True).where(PartNumber.part_no.like(query))
    return db.execute(stmt).all()
