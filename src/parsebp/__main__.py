import sys
from openpyxl import load_workbook

from .bosch_price import BoschPrice


def validate_argv(args: list) -> bool:
    # todo missing argument
    if len(args) != 2:
        raise SystemExit(f'Unknown arguments: {args[2:]}')
    return True


def process_bp(file_name: str) -> None:
    wb = load_workbook(file_name)
    bp = BoschPrice(wb)
    bp.populate_db()


if __name__ == '__main__':
    process_bp(sys.argv[1])
