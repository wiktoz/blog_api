import pytest

from src.main.db.models import User
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client

def test_get_me(client):
    auth = client.post('/api/auth/login', json={
        "email": "john.doe@example.com",
        "password": "password123"
    })

    atoken = auth.headers.getlist('Set-Cookie')[0].split(";")[0].split("=")[1]
    response = client.get('/api/users/me', headers={
        "Authorization": f"Bearer {atoken}",
        })
    assert response.status_code == 200
    assert response.json["email"] == "john.doe@example.com"

def test_get_user(client):
    auth = client.post('/api/auth/login', json={
        "email": "john.doe@example.com",
        "password": "password123"
    })
    user_id = User.query.filter_by(email="jane.smith@example.com").first().user_id
    atoken = auth.headers.getlist('Set-Cookie')[0].split(";")[0].split("=")[1]
    response = client.get(f'/api/users/{user_id}', headers={
        "Authorization": f"Bearer {atoken}",
        })
    assert response.status_code == 200
    assert response.json["email"] == "jane.smith@example.com"
    

def test_put_me(client):
    auth = client.post('/api/auth/login', json={
        "email": "john.doe@example.com",
        "password": "password123"
    })
    user_id = User.query.filter_by(email="jane.smith@example.com").first().user_id
    atoken = auth.headers.getlist('Set-Cookie')[0].split(";")[0].split("=")[1]
    x_csrf_token = auth.headers.getlist('Set-Cookie')[1].split(";")[0].split("=")[1]
    response = client.put(f'/api/users/me', headers={
        "Authorization": f"Bearer {atoken}",
        "X-CSRF-TOKEN": x_csrf_token
        }, json={"name":"Artur", "surname":"Tomaszewski"})
    assert response.status_code == 200
    assert response.json["name"] == "Artur"
    assert response.json["surname"] == "Tomaszewski"