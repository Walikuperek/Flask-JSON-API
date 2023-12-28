import uuid

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List

from ..models import PostDraft


@dataclass
class CreatePostDraftDto:
    title: str
    content: str
    author_id: str


@dataclass
class UpdatePostDraftDto:
    post_draft_id: str
    title: str | None = None
    content: str | None = None
    author_id: str | None = None


class PostDraftRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[PostDraft]:
        pass

    @abstractmethod
    def get_by_id(self, post_draft_id: str) -> PostDraft | None:
        pass

    @abstractmethod
    def create(self, dto: CreatePostDraftDto) -> PostDraft:
        pass

    @abstractmethod
    def update(self, dto: UpdatePostDraftDto) -> PostDraft | None:
        pass

    @abstractmethod
    def delete(self, post_draft_id: str) -> bool:
        pass


class InMemoryPostDraftRepository(PostDraftRepository):
    def __init__(self):
        self.post_drafts = []

    def get_all(self) -> List[PostDraft]:
        return self.post_drafts

    def get_by_id(self, post_draft_id: str) -> PostDraft | None:
        for post_draft in self.post_drafts:
            if post_draft.id == post_draft_id:
                return post_draft
        return None

    def create(self, dto: CreatePostDraftDto) -> PostDraft:
        post_draft = PostDraft(id=str(uuid.uuid4()),
                               title=dto.title,
                               content=dto.content,
                               author_id=dto.author_id,
                               created_at=datetime.utcnow())
        self.post_drafts.append(post_draft)
        return post_draft

    def update(self, dto: UpdatePostDraftDto) -> PostDraft | None:
        post_draft = self.get_by_id(dto.post_draft_id)
        if not post_draft:
            return None
        post_draft.title = dto.title or post_draft.title
        post_draft.content = dto.content or post_draft.content
        post_draft.author_id = dto.author_id or post_draft.author_id
        post_draft.updated_at = datetime.utcnow()
        post_draft.version += 1
        return post_draft

    def delete(self, post_draft_id: str) -> bool:
        post_draft = self.get_by_id(post_draft_id)
        if not post_draft:
            return False
        self.post_drafts.remove(post_draft)
        return True


draft_repo = InMemoryPostDraftRepository()
