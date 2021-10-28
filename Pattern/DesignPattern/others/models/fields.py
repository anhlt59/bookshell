from abc import ABCMeta


class Empty:
    pass


class Descriptor(metaclass=ABCMeta):
    def __set_name__(self, owner, name):
        self.name = name

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __set__(self, instance, value):
        value = self.clean(value)
        self.validate(value)
        # save cleaned data
        instance.__dict__[self.name] = value

    def serialize(self, value):
        return value

    def deserialize(self, value):
        return value

    def clean(self, value):
        return value

    def validate(self, value):
        return True


class Typed(Descriptor):
    class Meta:
        expected_type = type(None)
        default = None

    def __set_name__(self, owner, name):
        self._name = self._to_name or name

    def __init__(self, **kwargs):
        self.required = kwargs.pop("required", False)
        self.choices = kwargs.pop("choices", None)
        self.default = kwargs.pop("default", Empty if self.required else self.Meta.default)
        super().__init__(**kwargs)

    def clean(self, value):
        return value

    def validate(self, value):
        # value is not set
        if isinstance(value, Empty):
            raise TypeError(f"{self.__class__.__name__} is empty")
        # wrong expected type
        if not isinstance(value, self.Meta.expected_type):
            raise TypeError(
                f"{self.__class__.__name__} got value {value} Expected {self.Meta.expected_type}"
            )
        # check choice type, if not required and vaule == default > skip checking
        if self.choices and not (not self.required and value == self.default) and value not in self.choices:
            raise ValueError(
                f"{self.__class__.__name__} {value} is invalid, must be one of {self.choices}"
            )


class Integer(Typed):
    class Meta:
        expected_type = int
        default = 0


class Boolean(Typed):
    class Meta:
        expected_type = bool
        default = False


class List(Typed):
    class Meta:
        expected_type = list
        default = []


class String(Typed):
    class Meta:
        expected_type = str
        default = ""


class UrlField(String):
    def clean(self, value):
        return value.strip("/")
