import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
AWS_IGNORED_PROFILES = ("default", "anhlt", "session")
AWS_CREDENTIALS_DIR = os.getenv("AWS_CREDENTIALS_DIR", "~/.aws")
AWS_DEFAULT_PROFILE = os.getenv("AWS_DEFAULT_PROFILE", "default")
AWS_DEFAULT_SESSION_PROFILE = os.getenv("AWS_DEFAULT_SESSION_PROFILE", "session")

CACHE_FILE = os.getenv("CACHE_FILE") or os.path.join(BASE_DIR, ".cache")
DOWNLOADS_DIR = os.getenv("DOWNLOADS_DIR") or os.path.join(BASE_DIR, "downloads")

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S%z"
