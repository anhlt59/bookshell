import os
from concurrent.futures.thread import ThreadPoolExecutor
from threading import Lock


class SingletonMeta(type):
    _instances = {}
    _lock: "Lock" = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class ThreadExecutor(ThreadPoolExecutor, metaclass=SingletonMeta):

    def __init__(self, **kwargs):
        max_workers = kwargs.get("max_workers", int(os.getenv("MAX_WORKERS", 8)))
        super(ThreadExecutor, self).__init__(max_workers=max_workers, **kwargs)

    def __exit__(self, *args):
        return False

    def __del__(self):
        self.shutdown(wait=True)


# test
import time

os.environ["MAX_WORKERS"] = "2"


def sleep(n):
    time.sleep(n)
    print(f"sleep {n}s")


executor = ThreadExecutor()
executor.submit(sleep, 3)

executor = ThreadExecutor()
executor.submit(sleep, 2)

executor = ThreadExecutor()
executor.submit(sleep, 1)
