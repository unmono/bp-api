from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError

import schemas
from routers import products, login, users_manager

from settings import ApiSettings
settings = ApiSettings()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.CORS_ALLOWED_METHODS,
    allow_headers=settings.CORS_ALLOWED_HEADERS,
)

app.include_router(products.router)
app.include_router(login.router)
app.include_router(users_manager.router)


@app.exception_handler(RequestValidationError)
async def validation_exception(request, exc: RequestValidationError) -> JSONResponse:
    error_messages = [schemas.ValidationErrorSchema(
        loc=err['loc'][-1],
        msg=err['msg'].capitalize(),
    ) for err in exc.errors()]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({'detail': error_messages})
    )
