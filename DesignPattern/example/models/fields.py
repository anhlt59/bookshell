from abc import ABCMeta


class Descriptor(metaclass=ABCMeta):
    def __set_name__(self, owner, name):
        self._name = name

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __set__(self, instance, value):
        self.validate(value)
        instance.__dict__[self._name] = self.serialize(value)

    def serialize(self, value):
        return value

    def deserialize(self, value):
        return value

    def validate(self, value):
        return True


class Typed(Descriptor):
    expected_type = type(None)

    def __set_name__(self, owner, name):
        self._name = self._to_name or name

    def __init__(self, **kwargs):
        self._required = kwargs.pop("required", True)
        self._default = kwargs.pop("default", None)
        self._null = kwargs.pop("default", True)
        self._from_name = kwargs.pop("from_name", None)
        self._to_name = kwargs.pop("to_name", None)
        super().__init__(**kwargs)

    @property
    def name(self):
        return self._from_name or self._name

    @property
    def default(self):
        return self._default

    def validate(self, value):
        if value is not None:
            if not isinstance(value, self.expected_type):
                raise TypeError(f"Field {self._name} expected {self.expected_type}")
        else:
            if not self._null:
                raise TypeError(f"Field {self._name} is not null")


class IntegerField(Typed):
    expected_type = int


class BooleanField(Typed):
    expected_type = bool


class ListField(Typed):
    expected_type = list


class StringField(Typed):
    expected_type = str


class UrlField(Typed):
    expected_type = str

    def serialize(self, value: str):
        return value.strip("/")
