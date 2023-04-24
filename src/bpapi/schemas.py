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

    @root_validator
    def make_url(cls, values):
        # path_with_prefix = app.url_path_for('products_by_group', group_id=values['id'])
        path_with_prefix = f"/api/v1/sections/{values['id']}"
        path = '/' + '/'.join(path_with_prefix.split('/')[3:])
        values['path'] = path
        return values

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
    subsections: list[Section | Group]

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


class ListedPartnums(BaseModel):
    part_no: str = Field(example='AZ0910CHAR')
    title_en: str | None = Field(example='Product english description. \'None\' in case of refers list')
    path: str | None = Field(example='/path_to_detail/without/api/version')

    @root_validator
    def make_url(cls, values):
        # path_with_prefix = app.url_path_for('product', part_number=values['part_no'])
        path_with_prefix = f"/api/v1/products/{values['part_no']}"
        path = '/' + '/'.join(path_with_prefix.split('/')[3:])
        values['path'] = path
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
