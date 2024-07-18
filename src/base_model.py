import json
import os
from datetime import datetime, timezone

import pymongo
from bson import ObjectId


class BaseQuerySet:
    def __init__(self, table, model) -> None:
        self.table = table
        self.model = model
        mongo_url = os.environ.get("MONGO_URL")
        mongo_client = pymongo.MongoClient(mongo_url)
        db_name = os.environ.get("DB_NAME")
        self.db = mongo_client[db_name]
        self.collection = self.db[self.table]

    def _get_item_by_id(self, id):
        return self.collection.find_one({"_id": ObjectId(id)})

    def filter(self):
        query = {}
        return self.collection.find(query)

    def get(self, id):
        return self._get_item_by_id(id)

    def create(self, item):
        result = self.collection.insert_one(item)
        item = self._get_item_by_id(result.inserted_id)
        return item

    def partial_update(self, id, data):
        query = {"_id": ObjectId(id)}
        update_query = {"$set": data}
        result = self.collection.update_one(query, update_query)
        # TODO: Use result
        item = self._get_item_by_id(id)
        return item

    def delete(self, id):
        query = {"_id": ObjectId(id)}
        update_query = {"$set": {"deleted_at": datetime.now(timezone.utc)}}
        result = self.collection.update_one(query, update_query)
        # TODO: Use result

        item = self._get_item_by_id(id)
        return item


class ModelFactory:
    def build_item(self, model, data):
        cast_attrs = {}
        attrs = list(model.__dataclass_fields__.keys())
        for attr in attrs:
            type_cast = model.__dataclass_fields__[attr].type
            if not data[attr]:
                cast_attrs[attr] = None
            elif type_cast == datetime:
                cast_attrs[attr] = datetime.fromisoformat(data[attr])
            else:
                cast_attrs[attr] = type_cast(data[attr])
        return model(**cast_attrs)
