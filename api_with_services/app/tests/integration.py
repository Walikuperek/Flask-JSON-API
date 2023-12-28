import json
import pytest


@pytest.fixture
def setup_draft_post_response(client):
    create_draft_response = client.post(
        "/blog_posts/draft/",
        data=json.dumps(test_posts["resize_image_post"]),
        content_type="application/json",
    )
    assert create_draft_response.status_code == 200
    yield create_draft_response


# Tests
test_posts = {
    "resize_image_post": {
        "title": "Resize image with Python",
        "content": "Learn how to resize image with Python",
        "author_id": "user_OAIJSDOIJ"
    }
}


def test_make_post_from_draft(client, setup_draft_post_response):
    draft_id = json.loads(setup_draft_post_response.data)['id']
    publish_draft_response = client.post(f"/blog_posts/draft/{draft_id}/publish")
    assert publish_draft_response.status_code == 200
    assert json.loads(publish_draft_response.data)["published"]

    # Teardown - Delete post
    created_blog_post_id = json.loads(publish_draft_response.data)["blog_post"]["id"]
    delete_post_response = client.delete(f"/blog_posts/{created_blog_post_id}")
    assert delete_post_response.status_code == 200


def test_make_post_from_draft_with_invalid_draft_id(client):
    publish_draft_response = client.post(f"/blog_posts/draft/invalid_draft_id/publish")
    assert publish_draft_response.status_code == 404
    assert not json.loads(publish_draft_response.data)["published"]


# Below tests are same as simple_api/app/tests/integration.py tests
def test_get_blog_posts(client):
    get_all_posts_response = client.get("/blog_posts/")
    assert get_all_posts_response.status_code == 200
    assert json.loads(get_all_posts_response.data) == {"blog_posts": []}  # empty list for now


def test_create_blog_post(client):
    create_post_response = given_a_blog_post_exists(client, blog_post_data=test_posts["resize_image_post"])
    assert create_post_response["title"] == test_posts["resize_image_post"]["title"]
    assert create_post_response["content"] == test_posts["resize_image_post"]["content"]
    assert create_post_response["author_id"] == test_posts["resize_image_post"]["author_id"]


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
        blog_post_data = test_posts["resize_image_post"]
    response = client.post(
        "/blog_posts/",
        data=json.dumps(blog_post_data),
        content_type="application/json",
    )
    assert response.status_code == 200
    return json.loads(response.data)
