from openpyxl import Workbook, load_workbook


def load_bp(bp_file: str) -> Workbook:
    wb = load_workbook(bp_file, read_only=True)

    return wb


if __name__ == '__main__':
    pass
