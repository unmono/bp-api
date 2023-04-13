from pydantic import (
    BaseSettings
)


class ApiSettings(BaseSettings):
    # Routing
    ROUTE_PREFIX: str = '/api/v1'

    # CORS
    CORS_ALLOWED_ORIGINS: list[str] = [
        'http://localhost:5173',
    ]
    CORS_ALLOWED_METHODS: list[str] = [
        'GET',
        'POST'
    ]
    CORS_ALLOWED_HEADERS: list[str] = [
        '*'
    ]

    # Database:
    DATABASE_URL: str = '../bp.sqlite'

    # Authentication
    AUTH_KEY: str
    AUTH_ALG: str = 'HS256'
    TOKEN_EXPIRE_HOURS: int = 6

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
