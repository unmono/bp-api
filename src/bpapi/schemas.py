from __future__ import annotations
import re
from decimal import Decimal
from typing import ClassVar
from pydantic import (
    BaseModel,
    AnyUrl,
    validator,
    root_validator,
    constr,
    Field,
    PrivateAttr
)
from pydantic.dataclasses import dataclass

from app import app
import settings
settings = settings.ApiSettings()


class Group(BaseModel):
    id: int
    relative_url: str | None
    title: str

    # @validator('relative_url', pre=True)
    # def make_url(cls, router_path: str) -> str:
    #     """
    #     Transform relative path to absolute
    #     :param router_path: relative url from FastAPI.url_path_for()
    #     :return: absolute url
    #     """

    @root_validator
    def make_url(cls, values):
        values['relative_url'] = app.url_path_for('products_by_group', group_id=values['id'])
        return values

    class Config:
        orm_mode = True


class Section(BaseModel):
    title: str
    subsections: list[Section | Group]


class ListedPartnums(BaseModel):
    url: AnyUrl | None
    part_no: str
    title_en: str | None

    @root_validator
    def make_url(cls, values):
        part_no = values['part_no']
        values['url'] = f'http://localhost:8000/products/{part_no}'
        return values

    class Config:
        orm_mode = True


class Product(BaseModel):
    title_ua: str
    title_en: str
    uktzed: int
    min_order: int
    quantity: int
    price: Decimal
    truck: bool
    group: Group

    class Config:
        orm_mode = True


class MasterData(BaseModel):
    ean: int
    gross: Decimal
    net: Decimal
    weight_unit: str
    length: int
    width: int
    height: int
    measure_unit: str
    volume: Decimal
    volume_unit: str

    class Config:
        orm_mode = True


class PartNumber(BaseModel):
    part_no: str
    discontinued: bool
    new_release: bool
    product: Product | None
    masterdata: MasterData | None
    refers: list[ListedPartnums]

    class Config:
        orm_mode = True


class SearchRequest(BaseModel):
    search_query: constr(
        strip_whitespace=True,
        to_upper=True,
        min_length=10,
        max_length=10
    )

    @validator('search_query')
    def convert_search_query(cls, v):
        if not re.match(r'^([A-Z0-9]*[?]?[A-Z0-9]*){0,4}$', v):
            raise ValueError('Use only letters and digits. '
                             'You can replace missing character by ? up to 4 times.')
        return v.replace('?', '_')

