import os
import pickle
from typing import Any

from clitool.base import SingletonMeta
from clitool.settings import CACHE_FILE

__all__ = ["cache"]


class FileCache(metaclass=SingletonMeta):
    path: str
    data: dict[str, Any]

    def __init__(self, path: str = CACHE_FILE):
        self.path = path
        self.data = self.load()

    def load(self) -> dict[str, Any]:
        if not os.path.exists(self.path):
            return {}
        with open(self.path, "rb") as f:
            return pickle.load(f)

    def save(self):
        if not os.path.exists(os.path.dirname(self.path)):
            os.makedirs(self.path, exist_ok=True)
        with open(self.path, "wb") as f:
            pickle.dump(self.data, f)

    def set(self, key: str, value: Any):
        self.data[key] = value
        self.save()

    def mset(self, kwargs: dict[str, Any]):
        for key, value in kwargs.items():
            self.set(key, value)
        self.save()

    def get(self, key: str) -> Any:
        return self.data.get(key)

    def delete(self, key: str):
        del self.data[key]

    def clear(self):
        self.data = {}


cache = FileCache()
