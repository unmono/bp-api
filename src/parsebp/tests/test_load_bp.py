import pytest
import os
import sys
from openpyxl import Workbook

from parsebp.__main__ import load_bp


class TestLoadBP:

    regular_file = 'parsebp/tests/regular.xlsx'

    def test_load_regular_file(self):
        bp = load_bp(self.regular_file)
        assert isinstance(bp, Workbook), f'Result must be openpyxl.Workbook instance. ' \
                                         f'{type(bp)} given.'
