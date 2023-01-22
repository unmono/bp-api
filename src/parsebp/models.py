import re

from pydantic import BaseSettings, BaseModel
from functools import cached_property
from typing import ClassVar


class PriceList(BaseModel):
    _table_name: str = 'pricelist'
    sheet_pattern: ClassVar[re.Pattern] = re.compile(r'pricelist', re.I)

    class Config:
        underscore_attrs_are_private = False
