from src.base_router import BaseRouter
from src.models.user import User, UserQuerySet


class UserRouter(BaseRouter):
    def __init__(self):
        self.path = "/users"
        self.model = User
        self.queryset = UserQuerySet
        super().__init__()

    def create(self, item: User):
        return super().create(item)
