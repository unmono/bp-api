import sys
from openpyxl import load_workbook

from .bosch_price import BoschPrice
from unmonostuff.perfomance_tools import execution_timer


def validate_argv(args: list) -> bool:
    if len(args) != 2:
        raise SystemExit(f'Unknown arguments: {args[2:]}')
    return True


@execution_timer
def process_bp(file_name: str) -> None:
    wb = load_workbook(file_name)
    bp = BoschPrice(wb)
    bp.populate_db()


if __name__ == '__main__':
    process_bp(sys.argv[1])
