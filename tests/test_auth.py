import pytest

from app import create_app

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client

def test_register(client):
    response = client.post('/api/auth/register', json={
        "name": "john",
        "surname": "doe",
        "password": "V3rys3cvr3P@ssw0rd",
        "email": "test@test.com"
    })
    assert response.status_code == 200
    assert response.json == {"message":"Account created"}

def test_login(client):
    response = client.post('/api/auth/login', json={
        "email": "john.doe@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert response.json == {"login":True}

def test_invalid_register(client):
    response = client.post('/api/auth/register', json={
        "name": "john",
        "surname": "doe",
        "password": "1234567890",
        "email": "test2@test.com"
    })
    assert response.status_code == 401
    assert response.json == {"message":"Insecure password. Provided password is compromised"}

def test_invalid_login(client):
    response = client.post('/api/auth/login', json={
        "email": "john.doe@example.com",
        "password": "InvalidPassword"
    })
    assert response.status_code == 401
    assert response.json == {"login":False,"message":"Invalid credentials"}

def test_revoke_access_token(client):
    auth = client.post('/api/auth/login', json={
        "email": "john.doe@example.com",
        "password": "password123"
    })

    atoken = auth.headers.getlist('Set-Cookie')[0].split(";")[0].split("=")[1]
    x_csrf_token = auth.headers.getlist('Set-Cookie')[1].split(";")[0].split("=")[1]
   
    response = client.post('/api/auth/token/revoke/atoken', headers={
        "Authorization": f"Bearer {atoken}",
        "X-CSRF-TOKEN": x_csrf_token
    })
    assert response.status_code == 200
    assert response.json == {"logout":True}

def test_revoke_access_token(client):
    auth = client.post('/api/auth/login', json={
        "email": "john.doe@example.com",
        "password": "password123"
    })

    atoken = auth.headers.getlist('Set-Cookie')[0].split(";")[0].split("=")[1]
    x_csrf_token = auth.headers.getlist('Set-Cookie')[3].split(";")[0].split("=")[1]
   
    response = client.post('/api/auth/token/revoke/rtoken', headers={
        "Authorization": f"Bearer {atoken}",
        "X-CSRF-TOKEN": x_csrf_token
    })
    assert response.status_code == 200
    assert response.json == {"logout":True}


def test_refresh_token(client):
    auth = client.post('/api/auth/login', json={
        "email": "john.doe@example.com",
        "password": "password123"
    })
    atoken = auth.headers.getlist('Set-Cookie')[0].split(";")[0].split("=")[1]
    x_csrf_token = auth.headers.getlist('Set-Cookie')[3].split(";")[0].split("=")[1]
    response = client.post('/api/auth/token/refresh', headers={
        "Authorization": f"Bearer {atoken}",
        "X-CSRF-TOKEN": x_csrf_token
    })
    assert response.status_code == 200
    assert response.json == {"refresh":True}