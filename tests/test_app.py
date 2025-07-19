from http import HTTPStatus

from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_read_root_deve_retornar_ok_e_ola_mundo():
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello, World!'}


def test_read_root_deve_retornar_erro_404_para_url_inexistente():
    response = client.get('/inexistente')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Not Found'}


def test_read_root_deve_retornar_erro_405_para_metodo_nao_permitido():
    response = client.post('/')
    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
    assert response.json() == {'detail': 'Method Not Allowed'}
