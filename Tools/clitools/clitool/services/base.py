from clitool.base import SingletonMeta
from clitool.types.session import Session


class AwsService(metaclass=SingletonMeta):
    session: Session

    def __init__(self, session: Session, *args, **kwargs):
        self.session = session


class AwsSession(metaclass=SingletonMeta):
    pass
