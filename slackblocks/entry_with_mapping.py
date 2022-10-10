import json
from abc import ABC
from typing import Any


class EntryWithMapping(ABC):
    def to_dict(self) -> dict[str, Any]:
        return self.resolve()

    def json(self) -> str:
        return json.dumps(self.resolve(), indent=4)

    def __repr__(self) -> str:
        return self.json()

    def __getitem__(self, item):
        return self.resolve()[item]

    def keys(self) -> dict[str, Any]:
        return self.resolve()

    def resolve(self):
        """
        Resolves the entry.
        Returns a dict with the specified entry data.
        """
