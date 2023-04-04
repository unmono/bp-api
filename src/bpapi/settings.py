from pydantic import (
    BaseSettings,
    AnyHttpUrl
)


class ApiSettings(BaseSettings):
    host: str = 'http://localhost:8000'
    route_prefix: str = '/api/v1'

