import re

from decimal import Decimal
from pydantic import (
    BaseModel,
    validator,
    constr,
    Field,
)
from typing import ClassVar, Any, Optional


from parse_settings import ParseSettings
settings = ParseSettings()


class BPModel(BaseModel):
    table_name: ClassVar[str] = None

    @classmethod
    def sql_title(cls):
        return cls.table_name or cls.schema()['title'].lower()

    @classmethod
    def sqlite_schema(cls):
        title = cls.sql_title()
        sqlite_types = {
            'string': 'TEXT',
            'integer': 'INTEGER',
            'bool': 'INTEGER',
        }
        list_of_columns = []
        for field_title, properties in cls.schema()['properties'].items():
            if not (field_type := properties.get('type')):
                field_type = properties.get('anyOf')[0]['type']
            sql_type = sqlite_types[field_type]
            list_of_columns.append(f'{field_title} {sql_type}')
        columns_str = ', '.join(list_of_columns)
        return f'CREATE TABLE IF NOT EXISTS {title}({columns_str});'

    class Config:
        validate_assignment = True


class PriceList(BPModel):
    sheet_pattern: ClassVar[re.Pattern] = re.compile(r'pricelist', re.I)

    part_no: constr(
        strip_whitespace=True,
        regex=settings.PARTNO_PATTERN,
    ) = Field(excel_column='A')
    title_ua: constr(
        strip_whitespace=True,
        regex=settings.TITLE_UA_PATTERN,
    ) = Field(excel_column='B')
    title_en: Optional[constr(
        strip_whitespace=True,
        regex=settings.TITLE_EN_PATTERN,
    )] = Field(excel_column='C')
    sect: constr(
        strip_whitespace=True,
        regex=settings.SECTION_PATTERN,
    ) = Field(excel_column='F')
    subsect: constr(
        strip_whitespace=True,
        regex=settings.SUBSECTION_PATTERN,
    ) = Field(excel_column='G')
    subsub: constr(
        strip_whitespace=True,
        regex=settings.GROUP_PATTERN,
    ) = Field(excel_column='H')
    uktzed: Optional[int] = Field(excel_column='I')
    min_order: int = Field(excel_column='J')
    quantity: int = Field(excel_column='K')
    # price: Decimal = Field(excel_column='M')
    price: constr(
        strip_whitespace=True,
        regex=settings.DECIMAL_PATTERN,
    ) = Field(excel_column='M')
    truck: int | str | None = Field(excel_column='P')

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


class MasterData(BPModel):
    sheet_pattern: ClassVar[re.Pattern] = re.compile(r'master data', re.I)

    part_no: constr(
        strip_whitespace=True,
        regex=settings.PARTNO_PATTERN,
    ) = Field(excel_column='A')
    ean: Optional[int] = Field(excel_column='B')
    gross: Optional[constr(
        strip_whitespace=True,
        regex=settings.DECIMAL_PATTERN,
    )] = Field(excel_column='C')
    net: Optional[constr(
        strip_whitespace=True,
        regex=settings.DECIMAL_PATTERN,
    )] = Field(excel_column='D')
    weight_unit: Optional[constr(strip_whitespace=True, regex='^KG$|^kg$|^Kg$')] = Field(excel_column='E')
    length: Optional[int] = Field(excel_column='F')
    width: Optional[int] = Field(excel_column='G')
    height: Optional[int] = Field(excel_column='H')
    measure_unit: Optional[constr(strip_whitespace=True, regex='^MM$|^mm$|^Mm$')] = Field(excel_column='I')
    volume: Optional[constr(
        strip_whitespace=True,
        regex=settings.DECIMAL_PATTERN,
    )] = Field(excel_column='J')
    volume_unit: Optional[constr(strip_whitespace=True, regex='^L$|^l$')] = Field(excel_column='K')


class NewRelease(BPModel):
    sheet_pattern: ClassVar[re.Pattern] = re.compile(r'new release|новий', re.I)

    part_no: constr(
        strip_whitespace=True,
        regex=settings.PARTNO_PATTERN,
    ) = Field(excel_column='A')


class Discontinued(BPModel):
    sheet_pattern: ClassVar[re.Pattern] = re.compile(r'зняті', re.I)

    part_no: constr(
        strip_whitespace=True,
        regex=settings.PARTNO_PATTERN,
    ) = Field(excel_column='A')


class References(BPModel):
    table_name = 'refs'
    sheet_pattern: ClassVar[re.Pattern] = re.compile(r'Замін', re.I)

    predecessor: constr(
        strip_whitespace=True,
        regex=settings.PARTNO_PATTERN,
    ) = Field(excel_column='A')
    successor: constr(
        strip_whitespace=True,
        regex=settings.PARTNO_PATTERN
    ) = Field(excel_column='B')
