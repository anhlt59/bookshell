from collections import OrderedDict
from typing import Dict, List

from Pattern.DesignPattern.others.models.fields import Descriptor, StringField, IntegerField


class InvalidValue(Exception):
    pass


class ModelMeta(type):
    class Meta:
        ordering = ()
        descriptiors = {}

    def __new__(mcs, clsname, bases, methods):
        if not methods.get("Meta"):
            methods.Meta = mcs.Meta

        # Attach descriptors to Meta
        methods.Meta.descriptiors = OrderedDict()
        for key, value in methods.items():
            if isinstance(value, Descriptor):
                methods.Meta.descriptiors[key] = value

        # create default ordering base on Meta.descriptors
        if not getattr(methods.Meta, "ordering", None):
            methods.Meta.ordering = methods.Meta.descriptiors.keys()
        return type.__new__(mcs, clsname, bases, methods)


class Model(metaclass=ModelMeta):

    def __init__(self, arg: Dict = None, **kwargs):
        # validate input
        if arg:
            if not isinstance(arg, dict):
                raise TypeError(f"Argument {arg} must be type of Dict")
            if kwargs:
                raise ValueError("Input is type of Dict or keyword agruments, not both")

        data = arg or kwargs
        for key, descriptior in self.Meta.descriptiors.items():
            value = data.get(descriptior.name, descriptior.default)
            try:
                setattr(self, key, value)
            except (TypeError, ValueError) as e:
                raise InvalidValue(key, str(e))

    @classmethod
    def load(cls, arg: Dict = None, **kwargs) -> "Model":
        # load xlsx data
        data = arg or kwargs
        result = {}

        for key, descriptior in cls.Meta.descriptiors.items():
            value = data.get(descriptior.name, descriptior.default)
            try:
                result[key] = descriptior.deserialize(value)
            except (TypeError, ValueError) as e:
                raise InvalidValue(key, str(e))
        return cls(result)

    def dump(self) -> List:
        # sort result by Meta.ordering
        data = self.__dict__
        descriptiors = self.Meta.descriptiors
        return [descriptiors[name].serialize(data.get(name)) for name in self.Meta.ordering]

    def validate(self, *args, **kwargs):
        pass

    def save(self):
        pass


# Test
class PeopleModel(Model):
    name = StringField(required=True, from_name="Name", to_name="__Name__")
    age = IntegerField(required=True, null=True)
    job = StringField(required=False, default="123")


test1 = PeopleModel(Name="anhlt", age=20, job="DEV")
print(test1.dump())

test2 = PeopleModel({"Name": "anhlt"})
print(test2.dump())
