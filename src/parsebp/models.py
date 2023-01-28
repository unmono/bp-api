import re
import sqlite3
import os

from pydantic import (
    BaseModel,
    validator,
    constr,
    Field,
)
from typing import ClassVar, Any
from decimal import Decimal


from settings import ParseSettings
settings = ParseSettings()


class PriceList(BaseModel):
    sheet_pattern: ClassVar[re.Pattern] = re.compile(r'pricelist', re.I)

    part_no: constr(
        strip_whitespace=True,
        regex=settings.PARTNO_PATTERN,
    ) = Field(excel_column='A')
    title_ua: constr(
        strip_whitespace=True,
        regex=settings.TITLE_UA_PATTERN,
    ) = Field(excel_column='B')
    title_en: constr(
        strip_whitespace=True,
        regex=settings.TITLE_EN_PATTERN,
    ) = Field(excel_column='C')
    section: constr(
        strip_whitespace=True,
        regex=settings.SECTION_PATTERN,
    ) = Field(excel_column='F')
    subsection: constr(
        strip_whitespace=True,
        regex=settings.SUBSECTION_PATTERN,
    ) = Field(excel_column='G')
    group: constr(
        strip_whitespace=True,
        regex=settings.GROUP_PATTERN,
    ) = Field(excel_column='H')
    uktzed: int = Field(excel_column='I')
    min_order: int = Field(excel_column='J')
    quantity: int = Field(excel_column='K')
    price: constr(
        strip_whitespace=True,
        regex=settings.DECIMAL_PATTERN,
    ) = Field(excel_column='M')
    truck: bool | str = Field(excel_column='P')

    @validator('truck')
    def parse_truck(cls, v: Any) -> bool:
        if not v:
            return False
        elif type(v) is str:
            return bool(v.strip())
        elif type(v) is bool:
            return v
        else:
            raise ValueError('The value of the Truck assortment must be str or bool')

    class Config:
        underscore_attrs_are_private = False
        validate_assignment = True


class MasterData(BaseModel):
    sheet_pattern: ClassVar[re.Pattern] = re.compile(r'master data', re.I)

    part_no: constr(
        strip_whitespace=True,
        regex=settings.PARTNO_PATTERN,
    ) = Field(excel_column='A')
    ean: int = Field(excel_column='B')
    gross: constr(
        strip_whitespace=True,
        regex=settings.DECIMAL_PATTERN,
    ) = Field(excel_column='C')
    net: constr(
        strip_whitespace=True,
        regex=settings.DECIMAL_PATTERN,
    ) = Field(excel_column='D')
    weight_unit: constr(strip_whitespace=True, regex='^KG$|^kg$|^Kg$') = Field(excel_column='E')
    length: int = Field(excel_column='H')
    width: int = Field(excel_column='I')
    height: int = Field(excel_column='J')
    measure_unit: constr(strip_whitespace=True, regex='^MM$|^mm$|^Mm$') = Field(excel_column='K')
    volume: constr(
        strip_whitespace=True,
        regex=settings.DECIMAL_PATTERN,
    ) = Field(excel_column='F')
    volume_unit: constr(strip_whitespace=True, regex='^L$|^l$') = Field(excel_column='G')

    class Config:
        validate_assignment = True


class NewRelease(BaseModel):
    sheet_pattern: ClassVar[re.Pattern] = re.compile(r'new release|новий', re.I)

    part_no: constr(
        strip_whitespace=True,
        regex=settings.PARTNO_PATTERN,
    ) = Field(excel_column='A')

    class Config:
        underscore_attrs_are_private = False
        validate_assignment = True


class Discontinued(BaseModel):
    sheet_pattern: ClassVar[re.Pattern] = re.compile(r'зняті', re.I)

    part_no: constr(
        strip_whitespace=True,
        regex=settings.PARTNO_PATTERN,
    ) = Field(excel_column='A')

    class Config:
        underscore_attrs_are_private = False
        validate_assignment = True


class References(BaseModel):
    sheet_pattern: ClassVar[re.Pattern] = re.compile(r'Замін', re.I)

    predecessor: constr(
        strip_whitespace=True,
        regex=settings.PARTNO_PATTERN,
    ) = Field(excel_column='A')
    successor: constr(
        strip_whitespace=True,
        regex=settings.PARTNO_PATTERN
    ) = Field(excel_column='B')

    class Config:
        underscore_attrs_are_private = False
        validate_assignment = True
