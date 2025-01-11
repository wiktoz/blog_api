import pytest

from app import create_app
from src.main.db.models import Group

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client


def test_get_groups(client):
    auth = client.post('/api/auth/login', json={
        "email": "john.doe@example.com",
        "password": "password123"
    })

    atoken = auth.headers.getlist('Set-Cookie')[0].split(";")[0].split("=")[1]
    group_id = Group.query.filter_by(name="Home Chefs").first().group_id
    response = client.get(f'/api/groups/{group_id}', headers={
        "Authorization": f"Bearer {atoken}",
        })
    assert response.status_code == 200
    assert response.json["name"] == "Home Chefs"

def test_invalid_get_group(client):
    auth = client.post('/api/auth/login', json={
        "email": "john.doe@example.com",
        "password": "password123"
    })

    atoken = auth.headers.getlist('Set-Cookie')[0].split(";")[0].split("=")[1]
    group_id = 9999999
    response = client.get(f'/api/groups/{group_id}', headers={
        "Authorization": f"Bearer {atoken}",
        })
    assert response.status_code == 404
    assert response.json["message"] == "No such group"


def test_join_group(client):
    auth = client.post('/api/auth/login', json={
        "email": "jane.smith@example.com",
        "password": "password123"
    })

    atoken = auth.headers.getlist('Set-Cookie')[0].split(";")[0].split("=")[1]
    group_id = Group.query.filter_by(name="Culinary Enthusiasts").first().group_id
    response = client.get(f'/api/groups/{group_id}/join', headers={
            "Authorization": f"Bearer {atoken}"
        }
    )
    assert response.status_code == 200
    assert response.json["message"] == "User joined group"

def test_invalid_join_group(client):
    auth = client.post('/api/auth/login', json={
        "email": "john.doe@example.com",
        "password": "password123"
    })

    atoken = auth.headers.getlist('Set-Cookie')[0].split(";")[0].split("=")[1]
    group_id = Group.query.filter_by(name="Home Chefs").first().group_id
    response = client.get(f'/api/groups/{group_id}/join', headers={
            "Authorization": f"Bearer {atoken}"
        }
    )
    assert response.status_code == 400
    assert response.json["message"] == "User already in group"

def test_get_posts(client):
    auth = client.post('/api/auth/login', json={
        "email": "john.doe@example.com",
        "password": "password123"
    })
    atoken = auth.headers.getlist('Set-Cookie')[0].split(";")[0].split("=")[1]
    group_id = Group.query.filter_by(name="Home Chefs").first().group_id
    response = client.get(f'/api/groups/{group_id}/posts', headers={
            "Authorization": f"Bearer {atoken}"
        }
    )
    assert response.status_code == 200

def test_invalid_get_posts(client):
    auth = client.post('/api/auth/login', json={
        "email": "jane.smith@example.com",
        "password": "password123"
    })
    atoken = auth.headers.getlist('Set-Cookie')[0].split(";")[0].split("=")[1]
    group_id = Group.query.filter_by(name="Culinary Enthusiasts").first().group_id
    response = client.get(f'/api/groups/{group_id}/posts', headers={
            "Authorization": f"Bearer {atoken}"
        }
    )
    assert response.status_code == 403
    assert response.json["message"] == "No permission"

def test_add_post(client):
    auth = client.post('/api/auth/login', json={
        "email": "john.doe@example.com",
        "password": "password123"
    })
    atoken = auth.headers.getlist('Set-Cookie')[0].split(";")[0].split("=")[1]
    x_csrf_token = auth.headers.getlist('Set-Cookie')[1].split(";")[0].split("=")[1]
    group_id = Group.query.filter_by(name="Home Chefs").first().group_id
    data = {
        "title": "New Recipe",
        "content": "This is a new recipe",
        "photos": ""
    }
    response = client.post(f'/api/groups/{group_id}/posts', headers={"Authorization": f"Bearer {atoken}", "X-CSRF-TOKEN": x_csrf_token}, json=data)
    assert response.status_code == 200

def test_invalid_add_post(client):
    auth = client.post('/api/auth/login', json={
        "email": "john.doe@example.com",
        "password": "password123"
    })
    atoken = auth.headers.getlist('Set-Cookie')[0].split(";")[0].split("=")[1]
    x_csrf_token = auth.headers.getlist('Set-Cookie')[1].split(";")[0].split("=")[1]
    group_id = Group.query.filter_by(name="Home Chefs").first().group_id
    data = {
        #"title": "New Recipe", MISSING DATA
        "content": "This is a new recipe",
        "photos": ""
    }
    response = client.post(f'/api/groups/{group_id}/posts', headers={"Authorization": f"Bearer {atoken}", "X-CSRF-TOKEN": x_csrf_token}, json=data)
    assert response.status_code == 400
    assert response.json["message"] == "Missing data"


def test_search_group_by_phrase(client):
    auth = client.post('/api/auth/login', json={
        "email": "john.doe@example.com",
        "password": "password123"
    })
    atoken = auth.headers.getlist('Set-Cookie')[0].split(";")[0].split("=")[1]
    response = client.get(f'/api/groups/search/home', headers={"Authorization": f"Bearer {atoken}"})
    print(response.json)
    assert response.status_code == 200
    assert len(response.json) == 1