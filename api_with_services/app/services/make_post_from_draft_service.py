from abc import ABC

from .blog_post_repository import CreatePostDto, PostRepository
from .post_draft_repository import PostDraftRepository
from ..models import BlogPost


class PostDraftNotFound(Exception):
    def __init__(self, post_draft_id: str):
        super().__init__(f"Post draft {post_draft_id} not found")


class MakePostFromDraft(ABC):
    def publish(self, post_draft_id: str) -> BlogPost:
        """
        Publish new post from a draft.
        :raises PostDraftNotFound: If post draft with given id doesn't exist
        :param post_draft_id: Source post draft id
        :return: BlogPost
        """


class MakePostFromDraftService(MakePostFromDraft):
    def __init__(self, draft_repo: PostDraftRepository, post_repo: PostRepository):
        self.post_draft_repo = draft_repo
        self.post_repo = post_repo

    def publish(self, post_draft_id: str) -> BlogPost:
        post_draft = self.post_draft_repo.get_by_id(post_draft_id)
        if post_draft is None:
            raise PostDraftNotFound(post_draft_id)
        blog_post = self.post_repo.create(CreatePostDto(title=post_draft.title,
                                                        content=post_draft.content,
                                                        author_id=post_draft.author_id))
        self.post_draft_repo.delete(post_draft_id)
        return blog_post


"""
Example of how we would use the service in our routes with a decorator pattern, used
when we want to send an email to author that post is published or add anything else.

class SendEmailThatPostIsPublished(MakePostFromDraft):
    def __init__(self, make_post_from_draft_service: MakePostFromDraftService):
        self.make_post_from_draft_service = make_post_from_draft_service

    def publish(self, post_draft_id: str) -> BlogPost:
        blog_post = self.make_post_from_draft_service.publish(post_draft_id)
        # Send email to author that post is published
        return blog_post


# This is how we would use the service in our routes
# We can stack services on top of each other with the decorator pattern
SendEmailThatPostIsPublished(
    MakePostFromDraftService(draft_repo=PostDraftRepository(),
                             post_repo=PostRepository())
).publish(post_draft_id="put_real_post_draft_id_here")
"""
