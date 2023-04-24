from __future__ import annotations
import re
from decimal import Decimal
from pydantic import (
    BaseModel,
    validator,
    root_validator,
    constr,
    Field,
)

import settings
settings = settings.ApiSettings()


class Group(BaseModel):
    id: int = Field(exclude=True)
    title: str
    path: str | None

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'title': 'Group title',
                'path': '/path_to_related_products/without/api/version'
            }
        }


class Section(BaseModel):

    title: str
    subsections: list[Section | Group]  # future annotation

    class Config:
        schema_extra = {
            'example': {
                'title': 'Section title',
                'subsections': [
                    {
                        'title': 'Subsection title',
                        'subsections': [
                            {
                                'title': 'Group title',
                                'path': '/path_to_related_products/without/api/version'
                            }
                        ]
                    }
                ]
            }
        }


part_no_field = Field(example='AZ0910CHAR')
title_en_field = Field(example='Product english description. \'None\' in case of refers list')


class ListedPartnums(BaseModel):
    part_no: str = part_no_field
    title_en: str | None = title_en_field
    path: str | None = Field(example='/path_to_detail/without/api/version')

    @root_validator
    def make_url(cls, values):
        values['path'] = f"/products/{values['part_no']}"
        return values

    class Config:
        orm_mode = True


class Product(BaseModel):
    title_ua: str = Field(example='Product ukrainian description')
    title_en: str = title_en_field
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
    part_no: str = part_no_field
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
    ) = Field(example='AZ0910????')

    @validator('search_query')
    def convert_search_query(cls, v):
        if not re.match(r'^([A-Z0-9]*[?]?[A-Z0-9]*){0,4}$', v):
            raise ValueError('Use only letters and digits. '
                             'You can replace missing character by ? up to 4 times.')
        return v.replace('?', '_')


class ValidationErrorSchema(BaseModel):
    loc: str = Field(example='field_caused_an_error')
    msg: str = Field(example='Error message')


class User(BaseModel):
    username: constr(
        strip_whitespace=True,
        min_length=3,
        max_length=25,
        regex=r'^[a-zA-Z0-9]+$',
    ) = Field(example='JohnSmith')


class UserValidation(User):
    password: constr(
        min_length=8,
        regex=r'^\S+$',
    )
    scopes: list[str] = ['catalogue', ]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(User):
    scopes: list[str] = []
