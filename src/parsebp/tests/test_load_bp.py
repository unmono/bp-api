import pytest
import os
import sys
from openpyxl import Workbook
from openpyxl.utils.exceptions import InvalidFileException

from parsebp.__main__ import load_bp
from parsebp.bosch_price import BoschPrice


class TestBoschPrice:

    regular_file = 'parsebp/tests/regular.xlsx'
    lazy_file = 'parsebp/tests/lazy.xlsx'
    no_master_data_file = 'parsebp/tests/no_master_data.xlsx'

    unsupported_file = 'parsebp/tests/' + os.path.basename(__file__)
    unsupported_file_structure = 'parsebp/tests/unsupported_file_structure.xlsx'

    def test_unsupported_load(self):
        with pytest.raises(InvalidFileException):
            BoschPrice(load_bp(self.unsupported_file))

    @classmethod
    def normal_load(cls, file=regular_file):
        bp = BoschPrice(load_bp(file))
        assert isinstance(bp.wb, Workbook), f'Result must be openpyxl.Workbook instance. ' \
                                            f'{type(bp)} given.'
        return bp

    @pytest.mark.parametrize(
        'bp_file, expected',
        [
            (regular_file, 0),
            (lazy_file, 1),
            (no_master_data_file, 0),
            (unsupported_file_structure, None),
        ]
    )
    def test_supported_file_structure(self, bp_file, expected):
        bp = self.normal_load(bp_file)
        assert bp._validate_structure == expected
