from abc import ABC, abstractmethod
from typing import Any


# Product
# ---------------------------------------------------
class Product(ABC):
    pass


class CodeProduct(Product):
    def __init__(self, name):
        self._values = [
            f"class {name}:",
            "    def __init__(self):",
        ]

    def add_field(self, key: str, value: Any) -> Product:
        self._values.append(f"        self.{key} = {value}")
        return self

    def __str__(self) -> str:
        return "\n".join(self._values)


# Builder
# ---------------------------------------------------
class Builder(ABC):
    @property
    @abstractmethod
    def product(self) -> Product:
        pass

    @abstractmethod
    def add_field(self, key: str, value: Any) -> None:
        pass


class CodeBuilder(Builder):
    def __init__(self, name) -> None:
        self._product = CodeProduct(name)

    @property
    def product(self) -> Product:
        return self._product

    def add_field(self, key: str, value: Any) -> Builder:
        self._product.add_field(key, value)
        return self

    def __str__(self):
        return str(self._product)


# Director
# ---------------------------------------------------
class Director:
    def __init__(self) -> None:
        self._builder = None

    @property
    def builder(self) -> Builder:
        return self._builder

    @builder.setter
    def builder(self, builder: Builder) -> None:
        self._builder = builder

    def build_code_product(self):
        self._builder.add_field("name", "''").add_field("age", "0")


if __name__ == '__main__':
    director = Director()
    code_builder = CodeBuilder("Person")

    director.builder = code_builder
    director.build_code_product()

    print(code_builder)
