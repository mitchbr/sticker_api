from src.base_model import BaseQuerySet, BaseModel
from uuid import uuid4, UUID
from datetime import datetime
from dataclasses import dataclass


class UserQuerySet(BaseQuerySet):
    def __init__(self) -> None:
        self.table = "users"
        self.model = User
        super().__init__(self.table, self.model)


@dataclass
class User(BaseModel):
    id: UUID = uuid4()
    first_name: str = ""
    last_name: str = ""
    username: str = ""
    created_at: datetime = datetime.now()
