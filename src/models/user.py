from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from src.base_model import BaseQuerySet


class UserQuerySet(BaseQuerySet):
    def __init__(self) -> None:
        self.table = "users"
        self.model = User
        super().__init__(self.table, self.model)


@dataclass
class User:
    id: UUID = uuid4()
    first_name: str = ""
    last_name: str = ""
    username: str = ""
    created_at: datetime = datetime.now()
