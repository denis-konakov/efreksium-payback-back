import fastapi
from fastapi.exceptions import RequestValidationError, ValidationError
from db import SessionLocal
from loguru import logger
from config import Config

from db import Base
import crud.db_models
Base.metadata.create_all()
from utils import HTTPResponseModel
from fastapi.openapi.utils import validation_error_definition
from fastapi.exception_handlers import http_exception_handler
from utils.response import ResponseException
app = fastapi.FastAPI(responses={
    422: {
        'description': 'Ошибка валидации данных',
        'content': {'application/json': {'example': {
            'detail': {
                'detail': 'Ошибка валидации данных',
                'program_code': 'validation_exception',
                'status': False,
                'response': [{
                    "loc": [
                        "string",
                        0
                      ],
                      "msg": "string",
                      "type": "string"
                }]
            }}}
        }
    }
})

from routes import router

app.include_router(router)


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: fastapi.Request, exc: RequestValidationError):
    return fastapi.responses.JSONResponse({
        'detail': {
            'status': False,
            'program_code': 'validation_exception',
            'detail': 'Произошла ошибка при валидации входных данных',
            'response': exc.errors()
        }}, status_code=422)

@app.exception_handler(ResponseException)
async def response_exception_handler(request: fastapi.Request, exc: ResponseException):
    return await http_exception_handler(request, exc.get())
