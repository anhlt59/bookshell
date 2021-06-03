from typing import Any, Protocol


# Rich interface
class RichItem(Protocol):
    columns: list

    def to_row(self) -> list[Any]:
        ...

    def serialize(self) -> dict:
        ...

    @classmethod
    def deserialize(cls, data: dict) -> "RichItem":
        ...
