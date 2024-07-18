from datetime import datetime

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

    def to_json(self, item):
        serialized_data = {}
        for key in item.keys():
            if key == "_id":
                serialized_data["id"] = str(item[key])
            elif type(item[key]) == datetime:
                serialized_data[key] = item[key].isoformat()
            else:
                serialized_data[key] = item[key]

        return serialized_data

    def get_collection(self):
        # TODO: Filtering
        collection = self.queryset.filter()
        serialized_collection = []
        for item in collection:
            serialized_collection.append(self.to_json(item))
        return {"data": serialized_collection}

    def fetch(self, id):
        item = self.to_json(self.queryset.get(id))
        return {"data": item}

    def partial_update(self, id, item: dict):
        item = self.queryset.partial_update(id, item)
        item_json = self.to_json(item)
        return {"data": item_json}

    def create(self, item):
        item = self.queryset.create(item)
        item_json = self.to_json(item)
        return {"data": item_json}
