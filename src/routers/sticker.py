from src.base_router import BaseRouter
from src.models.sticker import Sticker, StickerQuerySet


class StickerRouter(BaseRouter):
    def __init__(self):
        self.path = "/stickers"
        self.model = Sticker
        self.queryset = StickerQuerySet
        super().__init__()

    def create(self, item: Sticker):
        return super().create(item)
