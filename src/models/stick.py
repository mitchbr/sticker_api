from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from src.base_model import BaseQuerySet


class StickQuerySet(BaseQuerySet):
    def __init__(self) -> None:
        self.table = "sticks"
        self.model = Stick
        super().__init__(self.table, self.model)


@dataclass
class Stick:
    id: UUID = uuid4()
    created_at: datetime = datetime.now()
    last_seen_at: datetime = datetime.now()
    latitude: float = 0.0
    longitude: float = 0.0
    notes: str = ""
    placed_by_id: str = ""  # TODO: How to handle relationships?
    sticker_id: str = ""
