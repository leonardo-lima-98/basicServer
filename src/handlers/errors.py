# src/handlers/errors.py
from http import HTTPStatus

from fastapi import Request
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException

templates = Jinja2Templates(directory='templates')

async def not_found_handler(
    request: Request, exc: StarletteHTTPException
):
    status_code = HTTPStatus.NOT_FOUND
    return templates.TemplateResponse(
        'status_code_template.html',
        {
            'request': request,
            'title': status_code.phrase,
            'message': status_code.description,
            'class': 'failed',
            'status_code': status_code.value,
        },
        status_code=status_code.value,
    )
