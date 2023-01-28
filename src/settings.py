import re
from pydantic import BaseSettings


class ParseSettings(BaseSettings):

    # Path to raw bp db
    RAW_DB: str = './raw.sqlite'

    # Excel columns re.patterns
    PARTNO_PATTERN: str = r'^[0-9A-Z]{10}$'
    TITLE_UA_PATTERN: str = r'^[0-9A-Za-zА-Яа-яЇїІіЄєҐґ /&+=,.()\[\]\-\\]+$'
    TITLE_EN_PATTERN: str = r'^[0-9A-Za-z /&+=,.()\[\]\-\\]+$'
    SECTION_PATTERN: str = r'^\d. [0-9A-Za-z /&+=,.()\[\]\-\\]+$'
    SUBSECTION_PATTERN: str = r'^\d.\d. [0-9A-Za-z /&+=,.()\[\]\-\\]+$'
    GROUP_PATTERN: str = r'^\d.\d.\d. [0-9A-Za-z /&+=,.()\[\]\-\\]+$'
    DECIMAL_PATTERN: str = r'^\d+[.,]?\d*$'
