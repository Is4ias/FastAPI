from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from fastapi_zero.app import app
from fastapi_zero.schemas import UserPublic


@pytest.fixture
def client():
    return TestClient(app)


def test_root_deve_retornar_ola_mundo(client):
    response = client.get('/')

    assert response.json() == {'message': 'Olá Mundo!'}
    assert response.status_code == HTTPStatus.OK


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'Naeli',
            'email': 'Naeli@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'email': 'Naeli@example.com',
        'username': 'Naeli',
        'id': response.json().get('id')
    }


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user):
    response = client.put(
        '/users/1',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': 1,
    }


def test_delete_user(client, user):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}
