import os
import shutil
import sqlite3
from contextlib import closing

from unmonostuff.perfomance_tools import execution_timer


from parse_settings import ParseSettings
settings = ParseSettings()


def dealing_with_files(file_to_normalize: str = settings.NORMALIZED_DB,
                       raw_db: str = settings.RAW_DB) -> str:
    try:
        os.remove(file_to_normalize)
    except FileNotFoundError:
        pass

    if not os.path.isfile(raw_db):
        raise FileNotFoundError(f'Source file {raw_db} doesn\'t exist.')
    shutil.copy(raw_db, file_to_normalize, follow_symlinks=False)

    return file_to_normalize


def get_script(normalization_file: str = 'bp_normalization.sql') -> str:
    with open(normalization_file, 'r') as bpn:
        normalization = bpn.read()

    return normalization


@execution_timer
def run_normalization(db_filename: str, normalization_filename: str) -> None:
    with closing(sqlite3.connect(db_filename)) as db:
        db.executescript(normalization_filename)


if __name__ == '__main__':
    file_to_normalize = dealing_with_files()
    normalization_script = get_script()
    run_normalization(file_to_normalize, normalization_script)

