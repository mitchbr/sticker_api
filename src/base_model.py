import json
from datetime import datetime, timezone
from dataclasses import dataclass
from uuid import UUID


@dataclass
class BaseModel:
    def to_json(self):
        data_dict = self.__dict__
        serialized_data = {}
        for key in data_dict.keys():
            if type(data_dict[key]) == UUID:
                serialized_data[key] = str(data_dict[key])
            elif type(data_dict[key]) == datetime:
                serialized_data[key] = data_dict[key].isoformat()
            else:
                serialized_data[key] = data_dict[key]

        return serialized_data


class BaseQuerySet:
    def __init__(self, table, model) -> None:
        self.table = table
        self.model = model

    def _get_raw_data(self):
        with open(f"src/data/{self.table}.json") as f:
            return json.load(f)

    def _load_data(self):
        return self._deserialize(self._get_raw_data())

    def _get_item_by_id(self, id):
        data = self._load_data()
        for item in data:
            if str(item.id) == id:
                return item

    def _deserialize(self, raw_data):
        items = []
        for row in raw_data["data"]:
            items.append(ModelFactory().build_item(self.model, row))
        return items

    def filter(self):
        return self._load_data()

    def get(self, id):
        return self._get_item_by_id(id)

    def create(self, item):
        json_data = self.model.to_json(item)
        raw_data = self._get_raw_data()
        raw_data["data"].append(json_data)
        with open(f"src/data/{self.table}.json", "w") as outfile:
            json.dump(raw_data, outfile)
        return item

    def partial_update(self, id, data):
        item = self._get_item_by_id(id)
        for attr in data.keys():
            if not hasattr(item, attr):
                return None
            # TODO: deserialize correctly
            setattr(item, attr, data[attr])

        raw_data = self._get_raw_data()
        for index, entry in enumerate(raw_data["data"]):
            if entry["id"] == id:
                raw_data["data"][index] = self.model.to_json(item)
                continue

        with open(f"src/data/{self.table}.json", "w") as outfile:
            json.dump(raw_data, outfile)

        return item

    def delete(self, id):
        item = self._get_item_by_id(id)
        if not item:
            return
        item.deleted_at = datetime.now(timezone.utc)

        raw_data = self._get_raw_data()
        for index, entry in enumerate(raw_data["data"]):
            if entry["id"] == id:
                raw_data["data"][index] = self.model.to_json(item)
                continue

        with open(f"src/data/{self.table}.json", "w") as outfile:
            json.dump(raw_data, outfile)

        return item


class ModelFactory:
    def build_item(self, model, data):
        cast_attrs = {}
        attrs = list(model.__dataclass_fields__.keys())
        for attr in attrs:
            type_cast = model.__dataclass_fields__[attr].type
            if type_cast == datetime:
                cast_attrs[attr] = datetime.fromisoformat(data[attr])
            else:
                cast_attrs[attr] = type_cast(data[attr])
        return model(**cast_attrs)
