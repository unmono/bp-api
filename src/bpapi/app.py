from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from settings import ApiSettings
settings = ApiSettings()

app = FastAPI()
app.router.prefix = settings.route_prefix

origins = [
    'http://localhost:5173',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET', 'POST'],
    allow_headers=['*'],
)
