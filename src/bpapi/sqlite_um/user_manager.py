import contextlib
import os
import sqlite3
from typing import Generator


class UserAlreadyExists(Exception):
    pass


class UserDoesNotExist(Exception):
    pass


class DatabaseCorrupted(Exception):
    pass


class SQLiteUserManager:
    """
    Defines user management methods.
    Provides 'in' usage.
    Provides object[username] getting.
    Superuser should be created on initial setup.
    Superuser cannot be deleted through api.
    Superuser cannot be listed through api.
    """

    def __init__(
        self,
        database_path: str | bytes | os.PathLike = 'users.sqlite',
        table_name: str | None = 'users',
    ):
        # todo? kwargs user schema
        self.database_path = database_path
        self.table_name = table_name

    def __contains__(self, username: str) -> bool:
        with self._db_connection() as db:
            user_count = db.execute(
                f'SELECT COUNT(*) FROM {self.table_name} WHERE username=?;',
                (username, )
            ).fetchone()[0]
        assert user_count in (0, 1), 'Whoa, something crazy with the database!'
        return bool(user_count)

    def __getitem__(self, username: str):
        if username not in self:
            raise KeyError()
        return self.get_user_dict(username)

    def add_user(
        self,
        username: str,
        password: str,
        scopes: list[str] = None,
        su: bool = False,
    ) -> None:
        """
        Add new user.
        :param username: username
        :param password: plain password
        :param scopes: list of scope strings.
        :param su: add superuser. Should not be available through api.
        :return: None
        """
        if username in self:
            raise UserAlreadyExists('This username is already used.')
        scopes_str = ','.join(scopes) if scopes else ''
        data_to_insert = {
            'username': username,
            'password': password,
            'scopes': scopes_str,
            'su': su,
        }
        with self._db_connection() as db:
            with db:
                db.execute(f"""
                    INSERT INTO {self.table_name} 
                    VALUES (:username, :password, :scopes, :su);
                """, data_to_insert)

    def delete_user(self, username: str) -> None:
        with self._db_connection() as db:
            with db:
                db.execute(f"""
                    DELETE FROM {self.table_name}
                    WHERE username = ? AND su != 1;
                """, (username, ))

    def get_user_dict(self, username: str) -> dict[str, str | list[str]] | None:
        with self._db_connection() as db:
            values = db.execute(f"""
                SELECT username, password, scopes
                FROM {self.table_name}
                WHERE username = ?;
            """, (username, )).fetchone()
        if values:
            keys = ('username', 'password', 'scopes')
            user_dict = dict(zip(keys, values))
            user_dict['scopes'] = user_dict['scopes'].split(',')
            return user_dict

        raise UserDoesNotExist('User with this username doesn\'t exist.')

    def get_all_users(self) -> list[dict[str, str]]:
        with self._db_connection() as db:
            fetch_users = db.execute(f"""
                SELECT username 
                FROM {self.table_name}
                WHERE su != 1;
            """).fetchall()

        return [{'username': username} for username, in fetch_users]

    def _initial_setup(self) -> None:
        expected_table_structure = [
            ('username', 'TEXT'),
            ('password', 'TEXT'),
            ('scopes', 'TEXT'),
            ('su', 'INT'),  # superuser True/False
        ]
        with self._db_connection() as db:
            db.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    {','.join([' '.join(field_tuple) for field_tuple in expected_table_structure])}            
                );
            """)

            # todo? separate method
            results = db.execute("""
                SELECT name, type 
                FROM pragma_table_info(?);
            """, (self.table_name, )).fetchall()

            assert results == expected_table_structure, 'Table structure is not supported.'

    @contextlib.contextmanager
    def _db_connection(self) -> Generator[sqlite3.Connection, None, None]:
        conn = sqlite3.connect(self.database_path)
        try:
            yield conn
        finally:
            conn.close()
