import sys
import time
from openpyxl import load_workbook

from .bosch_price import BoschPrice


if __name__ == '__main__':
    start = time.perf_counter()
    if len(sys.argv) != 2:
        raise SystemExit('Too many arguments.')
    wb = load_workbook(sys.argv[1])

    bp = BoschPrice(wb)
    bp.populate_db()

    print(time.perf_counter() - start)
