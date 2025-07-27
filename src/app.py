import uvicorn
from http import HTTPStatus

from auth import get_token

from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.handlers import errors
from src.routes.bingo import route as bingo_route
from src.routes.glances import route as glances_route
from src.routes.login import route as login_route
from src.routes.main import route as main_route
from src.routes.users import route as users_route

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

app.include_router(main_route, tags=['Main'])

app.include_router(bingo_route, prefix='/bingo', tags=['Bingo'])
app.include_router(glances_route, prefix='/glances', tags=['Glances'])
app.include_router(login_route, prefix='/login', tags=['Login'])
app.include_router(users_route, prefix='/users', tags=['Users'])


app.add_exception_handler(HTTPStatus.NOT_FOUND, errors.not_found_handler)
# app.add_event_handler(500, errors.not_found_handler)

@app.get("/protegido")
def recurso_protegido(token: str = Depends(get_token)):
    return {"message": "Dados acessados com sucesso usando o token!", "token": token}


if __name__ == "__main__":
    uvicorn.run(
        "src.app:app",
        host="127.0.0.1",
        port=8888,
        reload=True
    )
