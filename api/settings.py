from pydantic import (
    BaseSettings
)


class DevSettings(BaseSettings):
    # Routing
    ROUTE_PREFIX: str = '/api/v1'

    # CORS
    CORS_ALLOWED_ORIGINS: list[str] = [
        'http://localhost:5173',
    ]
    CORS_ALLOWED_METHODS: list[str] = [
        'GET',
        'POST',
        'DELETE',
    ]
    CORS_ALLOWED_HEADERS: list[str] = [
        '*'
    ]

    # Databases:
    DATABASE_PATH: str = 'bp.sqlite'
    USERS_DB_PATH: str = 'users.sqlite'

    # Authentication
    AUTH_KEY: str
    AUTH_ALG: str = 'HS256'
    TOKEN_EXPIRE_HOURS: int = 6

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


class ProdSettings(DevSettings):
    pass


class ApiSettings(DevSettings):
    pass
