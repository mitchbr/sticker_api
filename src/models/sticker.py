from src.base_model import BaseQuerySet, BaseModel
from uuid import uuid4, UUID
from datetime import datetime
from dataclasses import dataclass


class StickerQuerySet(BaseQuerySet):
    def __init__(self) -> None:
        self.table = "stickers"
        self.model = Sticker
        super().__init__(self.table, self.model)

    def create(self, item):
        return super().create(item)


@dataclass
class Sticker(BaseModel):
    id: UUID = uuid4()
    created_at: datetime = datetime.now()
    deleted_at: datetime = datetime.now()
    title: str = ""
    printCount: int = 0
    version: str = "1.0.0"
    creator_id: str = ""  # TODO: relationships
