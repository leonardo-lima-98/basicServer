from http import HTTPStatus
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.schemas import Message, UserCreate, UserResponse

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')


# Rotas principais
@app.get('/', response_model=Message, status_code=HTTPStatus.OK)
def read_root():
    return {'message': 'Hello, World!', 'status_code': HTTPStatus.OK}


@app.exception_handler(404)
async def not_found_handler(request: Request, exc: StarletteHTTPException):
    return templates.TemplateResponse(
        '404.html', {'request': request}, status_code=HTTPStatus.NOT_FOUND
    )


@app.get('/health', response_model=Message, status_code=HTTPStatus.OK)
def health_check():
    return {'message': 'ok', 'status_code': HTTPStatus.OK}


database = []

# Rotas de usuario
@app.get('/users', response_model=list[UserResponse], status_code=HTTPStatus.OK)
def get_users():
    return database


@app.post('/users', response_model=UserResponse, status_code=HTTPStatus.CREATED)
def create_user(user: UserCreate):
    user = UserResponse(
        id=f'{uuid4()}',
        name=user.name,
        email=user.email,
    )
    database.append(user)

    return user


@app.get(
    '/users/{user_id}', response_model=UserResponse, status_code=HTTPStatus.OK
)
def get_user(user_id: str):
    return {'message': f'User {user_id}', 'status_code': HTTPStatus.OK}


@app.put('/users/{user_id}', response_model=Message, status_code=HTTPStatus.OK)
def update_user(user_id: str):
    return {'message': f'User {user_id} updated', 'status_code': HTTPStatus.OK}


# Rota para o Glances
@app.get('/glances')
async def render_panel_glances(request: Request):
    return templates.TemplateResponse(
        'glances.html', {'request': request}, status_code=HTTPStatus.OK
    )