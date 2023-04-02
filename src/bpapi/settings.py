from pydantic import (
    BaseSettings,
    AnyUrl
)


class Settings(BaseSettings):
    route_prefix: AnyUrl = '/api/v1'

