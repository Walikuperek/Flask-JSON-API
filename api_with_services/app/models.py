from dataclasses import dataclass
from datetime import datetime


@dataclass
class BlogPost:
    id: str
    title: str
    content: str
    author_id: str
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass
class PostDraft:
    id: str
    title: str
    content: str
    author_id: str
    version: int = 1
    created_at: datetime | None = None
    updated_at: datetime | None = None
