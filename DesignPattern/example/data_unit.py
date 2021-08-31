from abc import abstractmethod, ABCMeta
from typing import Any


class BaseUnit(metaclass=ABCMeta):
    default = None

    @classmethod
    @abstractmethod
    def convert(cls, value: Any):
        pass

    def __new__(cls, value: Any):
        value = cls.convert(value or cls.default)
        return super(BaseUnit, cls).__new__(cls, value)


class DataUnit(float, BaseUnit):
    unit = None
    symbol = None
    default = 0.0

    @classmethod
    def convert(cls, value: Any):
        if isinstance(value, DataUnit) and cls.unit != value.unit:
            value = round(value * pow(1024, value.unit - cls.unit), 5)
        return value

    def __str__(self):
        return f"{self.real} {self.symbol}"

    def __sub__(self, other):
        return self.__class__(self.real - self.convert(other))

    def __add__(self, other):
        return self.__class__(self.real + self.convert(other))

    def __gt__(self, other):
        return self.real > self.convert(other)

    def __ge__(self, other):
        return self.real >= self.convert(other)

    def __lt__(self, other):
        return self.real < self.convert(other)

    def __le__(self, other):
        return self.real <= self.convert(other)

    def __eq__(self, other):
        return self.real == self.convert(other)

    def __ne__(self, other):
        return self.real != self.convert(other)


class Byte(DataUnit):
    symbol = "B"
    unit = 0


class KiloByte(DataUnit):
    symbol = "KB"
    unit = 1


class MegaByte(DataUnit):
    symbol = "MB"
    unit = 2


class GigaByte(DataUnit):
    symbol = "GB"
    unit = 3


class TeraByte(DataUnit):
    symbol = "TB"
    unit = 4


# test
a = Byte(10240)
b = KiloByte(10)
print(KiloByte(a))
print(MegaByte(a))
print(a + b)
print(b - a)
print(b == a)
print('test', a <= 10241.0)
print(Byte(MegaByte(100)))

# work with json type
import json

total = TeraByte(1)
used = GigaByte(150)
remain = total - used
print(json.dumps(dict(name="anhlt", total=total, unit=total.symbol, remain=remain)))
