from functools import cached_property
from openpyxl import Workbook

from bp_settings import PriceList


class BoschPrice:
    """
    Represents a loaded Bosch price list.
    """

    def __init__(self, wb: Workbook):
        self.wb = wb

    @cached_property
    def _validate_structure(self) -> int | None:
        """
        Finds out if there is a pricelist sheet in loaded file.
        :return: index of pricelist sheet
        """
        for i, sheet in enumerate(self.wb.sheetnames):
            if PriceList.sheet_pattern.search(sheet):
                return i
        return None
