import re

from pydantic import (
    BaseModel,
    validator,
    constr,
)
from typing import ClassVar
from decimal import Decimal


from settings import ParseSettings
settings = ParseSettings()


class PriceList(BaseModel):
    sheet_pattern: ClassVar[re.Pattern] = re.compile(r'pricelist', re.I)

    part_no: constr(strip_whitespace=True, regex=settings.PARTNO_PATTERN)
    title_ua: constr(strip_whitespace=True, regex=settings.TITLE_UA_PATTERN)
    title_en: constr(strip_whitespace=True, regex=settings.TITLE_EN_PATTERN)
    section: constr(strip_whitespace=True, regex=settings.SECTION_PATTERN)
    subsection: constr(strip_whitespace=True, regex=settings.SUBSECTION_PATTERN)
    group: constr(strip_whitespace=True, regex=settings.GROUP_PATTERN)
    uktzed: int
    min_order: int
    quantity: int
    price: Decimal
    truck: bool

    @validator('price')
    def quantize_price(cls, v: Decimal):
        return v.quantize(Decimal('.01'))

    class Config:
        underscore_attrs_are_private = False
        validate_assignment = True


class MasterData(BaseModel):
    sheet_pattern: ClassVar[re.Pattern] = re.compile(r'master data', re.I)

    part_no: constr(strip_whitespace=True, regex=settings.PARTNO_PATTERN)
    ean: int
    gross: Decimal
    net: Decimal
    weight_unit: constr(strip_whitespace=True, regex=r'^KG$')
    length: int
    width: int
    height: int
    measure_unit: constr(strip_whitespace=True, regex=r'^MM$')
    volume: Decimal
    volume_unit: constr(strip_whitespace=True, regex=r'^L$')


class NewRelease(BaseModel):
    sheet_pattern: ClassVar[re.Pattern] = re.compile(r'new release|новий', re.I)

    part_no: constr(strip_whitespace=True, regex=settings.PARTNO_PATTERN)


class Discontinued(BaseModel):
    sheet_pattern: ClassVar[re.Pattern] = re.compile(r'зняті', re.I)

    part_no: constr(strip_whitespace=True, regex=settings.PARTNO_PATTERN)


class References(BaseModel):
    sheet_pattern: ClassVar[re.Pattern] = re.compile(r'Замін', re.I)

    predecessor: constr(strip_whitespace=True, regex=settings.PARTNO_PATTERN)
    successor: constr(strip_whitespace=True, regex=settings.PARTNO_PATTERN)
