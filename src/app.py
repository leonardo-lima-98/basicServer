from http import HTTPStatus, client
from uuid import uuid4

from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.schemas import Message, User, UserCreate, UserResponse

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')


# Rotas principais
@app.get('/')
def read_root(request: Request, status_code=HTTPStatus.OK):
    return templates.TemplateResponse(
        'status_code_template.html',
        {
            'request': request,
            'title': status_code.phrase,
            'message': 'Hello, World!',
            'class': 'success',
            'status_code': status_code.value,
        },
        status_code=status_code.value,
    )


@app.exception_handler(404)
async def not_found_handler(
    request: Request, exc: StarletteHTTPException, status_code=HTTPStatus.NOT_FOUND
):
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


@app.get('/health')
def health_check(request: Request, status_code=HTTPStatus.OK):
    return templates.TemplateResponse(
        'status_code_template.html',
        {
            'request': request,
            'title': status_code.phrase,
            'message': 'Health Check Success',
            'class': 'success',
            'status_code': status_code.value,
        },
        status_code=status_code.value,
    )


database = [
    User(
        id='e537577e-54b5-4ce7-8589-d6fc0fb5d79d',
        name='leonardo',
        email='leonardo@owner.com',
        password='owner123',
        job_title='owner',
    ),
    User(
        id='55fbe272-1143-45c5-9b71-f62a9296d430',
        name='admin',
        email='admin@manager.com',
        password='admin123',
        job_title='manager',
    ),
    User(
        id='dfd1591a-e706-4ab9-9726-5080be2a5d9a',
        name='user',
        email='user@developer.com',
        password='user123',
        job_title='developer',
    ),
    User(
        id='867ba3ee-366a-494c-a092-c67f59992150',
        name='operator',
        email='operator@operation.com',
        password='operator123',
        job_title='operation',
    ),
]


# Rotas de usuario
@app.get('/users', response_model=list[UserResponse], status_code=HTTPStatus.OK)
def get_users():
    return database


@app.post('/users', response_model=UserResponse, status_code=HTTPStatus.CREATED)
def create_user(user: UserCreate):
    user = User(
        id=f'{uuid4()}',
        name=user.name,
        email=f'{user.name}@{user.job_title}.com',
        job_title=user.job_title,
        password=user.password,
    )
    database.append(user)
    return user


@app.get('/users/{user_id}', response_model=UserResponse, status_code=HTTPStatus.OK)
def get_user():
    print([item.model_dump() for item in database])
    return {'message': 'Users', 'status_code': HTTPStatus.OK}


@app.put('/users/{user_id}', response_model=Message, status_code=HTTPStatus.OK)
def update_user(user_id: str):
    return {'message': f'User {user_id} updated', 'status_code': HTTPStatus.OK}


# Rota para o Glances
def check_server_up(host: str, port: int) -> bool:
    try:
        conn = client.HTTPConnection(host, port, timeout=2)
        conn.request('GET', '/')
        response = conn.getresponse()
        return response.status == HTTPStatus.OK
    except Exception:
        return False


@app.get('/glances', response_class=HTMLResponse)
def show_glances(
    request: Request,
    host: str = Query(default='localhost'),
    port: int = Query(default=80),
):
    # if port == None: port = 80
    glances_url = f'http://{host}:{port}'

    if check_server_up(host, port):
        return templates.TemplateResponse(
            'glances.html',
            {'request': request, 'glances_url': glances_url, 'status_code': HTTPStatus.OK},
            status_code=HTTPStatus.OK,
        )
    else:
        status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        return templates.TemplateResponse(
            'status_code_template.html',
            {
                'request': request,
                'title': status_code.phrase,
                'message': f'Não foi possível acessar {glances_url}',
                'class': 'failed',
                'status_code': status_code.value,
            },
            status_code=status_code.value,
        )
