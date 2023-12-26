import json
import pytest

from main import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# Tests
test_posts_data = {
    "resize_image": {
        "title": "Resize image with Python",
        "content": "Learn how to resize image with Python",
        "author_id": "user_OAIJSDOIJ"
    }
}


def test_get_blog_posts(client):
    get_all_posts_response = client.get("/blog_posts/")
    assert get_all_posts_response.status_code == 200
    assert json.loads(get_all_posts_response.data) == {"blog_posts": []}  # empty list for now


def test_create_blog_post(client):
    create_post_response = given_a_blog_post_exists(client, blog_post_data=test_posts_data["resize_image"])
    assert create_post_response["title"] == test_posts_data["resize_image"]["title"]
    assert create_post_response["content"] == test_posts_data["resize_image"]["content"]
    assert create_post_response["author_id"] == test_posts_data["resize_image"]["author_id"]


def test_get_blog_by_id_post(client):
    given_post_in_db = given_a_blog_post_exists(client)
    get_blog_by_id_response = client.get(f"/blog_posts/{given_post_in_db['id']}")
    assert get_blog_by_id_response.status_code == 200
    assert json.loads(get_blog_by_id_response.data) == {"blog_post": given_post_in_db}


def test_update_blog_post(client):
    given_post_in_db = given_a_blog_post_exists(client)
    fields_to_update = {"title": "Updated Title"}
    update_response = client.put(
        f"/blog_posts/{given_post_in_db['id']}",
        data=json.dumps(fields_to_update),
        content_type="application/json",
    )
    assert update_response.status_code == 200
    assert json.loads(update_response.data)["title"] == "Updated Title"


def test_delete_blog_post(client):
    given_post_in_db = given_a_blog_post_exists(client)
    response = client.delete(f"/blog_posts/{given_post_in_db['id']}")
    assert response.status_code == 200
    assert json.loads(response.data) == {"deleted": True}


# Helper functions
def given_a_blog_post_exists(client, blog_post_data=None):
    if blog_post_data is None:
        blog_post_data = test_posts_data["resize_image"]
    response = client.post(
        "/blog_posts/",
        data=json.dumps(blog_post_data),
        content_type="application/json",
    )
    assert response.status_code == 200
    return json.loads(response.data)
