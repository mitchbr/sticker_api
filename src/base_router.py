from fastapi import APIRouter
from .base_model import ModelFactory


class BaseRouter:
    def __init__(self):
        if not hasattr(self, "path"):
            self.path = "/"
        if not hasattr(self, "model"):
            raise AttributeError("Routers require a model")
        if not hasattr(self, "queryset"):
            raise AttributeError("Routers require a queryset")
        self.queryset = self.queryset()
        self.router = APIRouter()
        self.router.add_api_route(self.path, self.get_collection, methods=["GET"])
        self.router.add_api_route(self.path + "/{id}", self.fetch, methods=["GET"])
        self.router.add_api_route(
            self.path + "/{id}", self.partial_update, methods=["PATCH"]
        )
        self.router.add_api_route(self.path, self.create, methods=["POST"])

    def get_collection(self):
        collection = self.queryset.filter()
        serialized_collection = []
        for item in collection:
            serialized_collection.append(item.to_json())
        return {"data": serialized_collection}

    def fetch(self, id):
        item = self.queryset.get(id)
        return {"data": item}

    def partial_update(self, id, item: dict):
        item = self.queryset.partial_update(id, item)
        return {"data": item}

    def create(self, item):
        res = self.queryset.create(item)
        return res
