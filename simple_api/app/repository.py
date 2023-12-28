import uuid

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List

from .models import BlogPost


@dataclass
class CreatePostDto:
    title: str
    content: str
    author_id: str


@dataclass
class UpdatePostDto:
    post_id: str
    title: str | None = None
    content: str | None = None
    author_id: str | None = None


class PostRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[BlogPost]:
        pass

    @abstractmethod
    def get_by_id(self, post_id: str) -> BlogPost | None:
        pass

    @abstractmethod
    def create(self, dto: CreatePostDto) -> BlogPost:
        pass

    @abstractmethod
    def update(self, dto: UpdatePostDto) -> BlogPost | None:
        pass

    @abstractmethod
    def delete(self, post_id: str) -> bool:
        pass


class InMemoryBlogPostRepository(PostRepository):
    def __init__(self):
        self.posts = []

    def get_all(self) -> List[BlogPost]:
        return self.posts

    def get_by_id(self, post_id: str) -> BlogPost | None:
        for post in self.posts:
            if post.id == post_id:
                return post
        return None

    def create(self, dto: CreatePostDto) -> BlogPost:
        post = BlogPost(id=str(uuid.uuid4()),
                        title=dto.title,
                        content=dto.content,
                        author_id=dto.author_id)
        self.posts.append(post)
        return post

    def update(self, dto: UpdatePostDto) -> BlogPost | None:
        post = self.get_by_id(dto.post_id)
        if post is None:
            return None
        post.title = dto.title if dto.title else post.title
        post.content = dto.content if dto.content else post.content
        post.author_id = dto.author_id if dto.author_id else post.author_id
        post.updated_at = datetime.now()
        return post

    def delete(self, post_id: str) -> bool:
        post = self.get_by_id(post_id)
        if post is None:
            return False
        self.posts.remove(post)
        return True


post_repo = InMemoryBlogPostRepository()
