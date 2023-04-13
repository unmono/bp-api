from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from settings import ApiSettings
settings = ApiSettings()

app = FastAPI()
app.router.prefix = settings.ROUTE_PREFIX

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.CORS_ALLOWED_METHODS,
    allow_headers=settings.CORS_ALLOWED_HEADERS,
)
