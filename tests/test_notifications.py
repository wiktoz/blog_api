import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client

def test_notifications(client):
    auth = client.post('/api/auth/login', json={
        "email": "john.doe@example.com",
        "password": "password123"
    })
    atoken = auth.headers.getlist('Set-Cookie')[0].split(";")[0].split("=")[1]
    response = client.get('/api/notifications/me', headers={
        "Authorization": f"Bearer {atoken}",
        })
    assert response.status_code == 200
    