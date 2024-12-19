import pytest
from src.main.db.models import Post
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client

def test_get_my_posts(client):
    auth = client.post('/api/auth/login', json={
        "email": "john.doe@example.com",
        "password": "password123"
    })
    atoken = auth.headers.getlist('Set-Cookie')[0].split(";")[0].split("=")[1]
    response = client.get('/api/posts/me', headers={"Authorization": f"Bearer {atoken}"})
    assert response.status_code == 200
    assert len(response.json) == 1

def test_get_post(client):
    auth = client.post('/api/auth/login', json={
        "email": "john.doe@example.com",
        "password": "password123"
    })
    post_id = Post.query.filter_by(title="Baking Tips and Tricks").first().post_id
    atoken = auth.headers.getlist('Set-Cookie')[0].split(";")[0].split("=")[1]
    response = client.get(f'/api/posts/{post_id}', headers={"Authorization": f"Bearer {atoken}"})
    assert response.status_code == 200
    assert response.json["title"] == "Baking Tips and Tricks"

def test_delete_post(client):
    auth = client.post('/api/auth/login', json={
        "email": "john.doe@example.com",
        "password": "password123"
    })
    post_id = Post.query.filter_by(title="Welcome to Home Chefs").first().post_id
    atoken = auth.headers.getlist('Set-Cookie')[0].split(";")[0].split("=")[1]
    x_csrf_token = auth.headers.getlist('Set-Cookie')[1].split(";")[0].split("=")[1]
    response = client.delete(f'/api/posts/{post_id}', headers={"Authorization": f"Bearer {atoken}", "X-CSRF-TOKEN": x_csrf_token})
    assert response.status_code == 200
    assert response.json["message"] == "Post deleted"

def test_invalid_delete_post(client):
    auth = client.post('/api/auth/login', json={
        "email": "john.doe@example.com",
        "password": "password123"
    })
    post_id = Post.query.filter_by(title="Baking Tips and Tricks").first().post_id
    atoken = auth.headers.getlist('Set-Cookie')[0].split(";")[0].split("=")[1]
    x_csrf_token = auth.headers.getlist('Set-Cookie')[1].split(";")[0].split("=")[1]
    response = client.delete(f'/api/posts/{post_id}', headers={"Authorization": f"Bearer {atoken}", "X-CSRF-TOKEN": x_csrf_token})
    assert response.status_code == 403
    assert response.json["message"] == "No permission. You are not the author!"


def test_avarage_rating(client):
    auth = client.post('/api/auth/login', json={
        "email": "john.doe@example.com",
        "password": "password123"
    })
    post_id = Post.query.filter_by(title="Baking Tips and Tricks").first().post_id
    atoken = auth.headers.getlist('Set-Cookie')[0].split(";")[0].split("=")[1]
    response = client.get(f'/api/posts/{post_id}/rate', headers={"Authorization": f"Bearer {atoken}"})
    assert response.status_code == 200
    assert response.json["average"] == 4.0

def test_rate_post(client):
    auth = client.post('/api/auth/login', json={
        "email": "john.doe@example.com",
        "password": "password123"
    })
    post_id = Post.query.filter_by(title="Welcome to Home Chefs").first().post_id
    atoken = auth.headers.getlist('Set-Cookie')[0].split(";")[0].split("=")[1]
    x_csrf_token = auth.headers.getlist('Set-Cookie')[1].split(";")[0].split("=")[1]
    data = {
        "value": 5
    }
    response = client.post(f'/api/posts/{post_id}/rate', headers={"Authorization": f"Bearer {atoken}", "X-CSRF-TOKEN": x_csrf_token}, json=data)

    assert response.status_code == 200
    assert response.json["message"] == "Rating added"


def test_get_comments(client):
    auth = client.post('/api/auth/login', json={
        "email": "john.doe@example.com",
        "password": "password123"
    })
    post_id = Post.query.filter_by(title="Baking Tips and Tricks").first().post_id
    atoken = auth.headers.getlist('Set-Cookie')[0].split(";")[0].split("=")[1]
    response = client.get(f'/api/posts/{post_id}/comments', headers={"Authorization": f"Bearer {atoken}"})
    assert response.status_code == 200
    assert len(response.json) == 1

def test_add_comment(client):
    auth = client.post('/api/auth/login', json={
        "email": "john.doe@example.com",
        "password": "password123"
    })
    post_id = Post.query.filter_by(title="Welcome to Home Chefs").first().post_id
    atoken = auth.headers.getlist('Set-Cookie')[0].split(";")[0].split("=")[1]
    x_csrf_token = auth.headers.getlist('Set-Cookie')[1].split(";")[0].split("=")[1]
    data = {
        "content": "fajne"
    }
    response = client.post(f'/api/posts/{post_id}/comments', headers={"Authorization": f"Bearer {atoken}", "X-CSRF-TOKEN": x_csrf_token}, json=data)

    assert response.status_code == 200
    assert response.json["message"] == "Comment added"