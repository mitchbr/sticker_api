from src.base_router import BaseRouter
from src.models.stick import Stick, StickQuerySet


class StickRouter(BaseRouter):
    def __init__(self):
        self.path = "/sticks"
        self.model = Stick
        self.queryset = StickQuerySet
        super().__init__()

    def create(self, item: Stick):
        return super().create(item)
