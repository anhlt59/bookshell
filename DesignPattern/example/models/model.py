import inspect
from abc import ABCMeta, abstractmethod
from typing import Dict

from DesignPattern.example.models.fields import Descriptor, StringField, IntegerField, EmptyValue


class BaseModel(metaclass=ABCMeta):

    def __init__(self, arg: Dict = None, **kwargs):
        # validate input
        if arg and kwargs:
            raise ValueError("Input is type of Dict or keyword agruments")
        elif arg:
            if not isinstance(arg, dict):
                raise TypeError(f"Argument {arg} must be type of Dict")
            kwargs.update(arg)

        description_fields = inspect.getmembers(self, lambda x: isinstance(x, Descriptor))
        for key, description in description_fields:
            setattr(self, key, kwargs.get(description.name, description.default))

    @abstractmethod
    def to_dict(self):
        pass

    @abstractmethod
    def to_list(self):
        pass

    @abstractmethod
    def save(self):
        pass


class Model(BaseModel):
    class Meta:
        ordering = ()

    def to_dict(self):
        return self.__dict__

    def to_list(self):
        if self.Meta.ordering:
            # sort result if Meta.ordering is defined
            data = self.__dict__
            result = [data[name] for name in self.Meta.ordering]
        else:
            result = self.__dict__.values()
        return result

    def save(self):
        return None


# Test
class PeopleModel(Model):
    name = StringField(required=True, from_name="Name", to_name="__Name__")
    age = IntegerField(required=True, null=True)
    job = StringField(required=False, default="123")


test1 = PeopleModel(Name="anhlt", age=20, job="DEV")
print(test1.to_dict())
print(test1.to_list())

test2 = PeopleModel({"Name": "anhlt"})
print(test2.to_dict())
print(test2.to_list())
