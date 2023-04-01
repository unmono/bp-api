import re
from decimal import Decimal
from pydantic import (
    BaseModel,
    AnyUrl,
    validator,
    root_validator,
    constr,
    Field,
)
from pydantic.dataclasses import dataclass


class Subsub(BaseModel):
    url: AnyUrl | None
    title: str

    @validator('url', pre=True)
    def make_url(cls, router_path: str) -> str:
        """
        Transform relative path to absolute
        :param router_path: relative url from FastAPI.url_path_for()
        :return: absolute url
        """
        return f'http://localhost:8000{router_path}'

    class Config:
        orm_mode = True


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
    subsub: Subsub

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

