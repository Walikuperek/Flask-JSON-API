from flask import Blueprint, jsonify, request

from .services import draft_repo, post_repo, CreatePostDto, UpdatePostDto, MakePostFromDraftService, CreatePostDraftDto, \
    PostDraftNotFound


bp = Blueprint("blog_posts", __name__, url_prefix="/blog_posts")


@bp.route("/", methods=["GET"])
def get_blog_posts():
    return jsonify({"blog_posts": post_repo.get_all()})


@bp.route("/", methods=["POST"])
def create_blog_post():
    data = request.get_json()
    blog_post = post_repo.create(dto=CreatePostDto(title=data.get("title"),
                                                   content=data.get("content"),
                                                   author_id=data.get("author_id")))
    return jsonify(blog_post.__dict__)


@bp.route("/<blog_post_id>", methods=["GET"])
def get_blog_post(blog_post_id):
    return jsonify({"blog_post": post_repo.get_by_id(blog_post_id)})


@bp.route("/<blog_post_id>", methods=["PUT"])
def update_blog_post(blog_post_id):
    data = request.get_json()
    blog_post = post_repo.update(dto=UpdatePostDto(post_id=blog_post_id,
                                                   title=data.get("title"),
                                                   content=data.get("content")))
    return jsonify(blog_post.__dict__ if blog_post else {})


@bp.route("/<blog_post_id>", methods=["DELETE"])
def delete_blog_post(blog_post_id):
    return jsonify({"deleted": post_repo.delete(blog_post_id)})


# Rest of the CRUD endpoints for PostDrafts...

@bp.route("/draft/", methods=["POST"])
def create_post_draft():
    data = request.get_json()
    post_draft = draft_repo.create(dto=CreatePostDraftDto(title=data.get("title"),
                                                          content=data.get("content"),
                                                          author_id=data.get("author_id")))
    return jsonify(post_draft.__dict__)


@bp.route("/draft/<post_draft_id>", methods=["DELETE"])
def delete_post_draft(post_draft_id):
    return jsonify({"deleted": draft_repo.delete(post_draft_id)})


@bp.route("/draft/<post_draft_id>/publish", methods=["POST"])
def publish_post_draft(post_draft_id):
    try:
        blog_post = MakePostFromDraftService(draft_repo=draft_repo, post_repo=post_repo).publish(post_draft_id)
        return jsonify({"published": True, "blog_post": blog_post.__dict__})
    except PostDraftNotFound as error:
        return jsonify({"published": False, "error": str(error)}), 404
