import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
AWS_IGNORED_PROFILES = ("default", "anhlt", "session")
AWS_CREDENTIALS_DIR = os.getenv("AWS_CREDENTIALS_DIR", "~/.aws")
AWS_DEFAULT_PROFILE = os.getenv("AWS_DEFAULT_PROFILE", "default")
AWS_DEFAULT_SESSION_PROFILE = os.getenv("AWS_DEFAULT_SESSION_PROFILE", "session")

CACHE_FILE = os.getenv("CACHE_FILE") or os.path.join(BASE_DIR, ".cache")
DOWNLOADS_DIR = os.getenv("DOWNLOADS_DIR") or os.path.join(BASE_DIR, "downloads")

PROJECT_ROLES = [
    {
        "profile": "di2dev",
        "arn": "arn:aws:iam::322940739131:mfa/neos-vietha",
    },
    {
        "profile": "di2prod",
        "arn": "arn:aws:iam::556975058824:mfa/neos-vietha",
    },
    {
        "profile": "neos",
        "arn": "arn:aws:iam::251123607109:mfa/anhlt",
    },
    {
        "profile": "neos",
        "arn": "arn:aws:iam::251123607109:role/di2-least-privileged-ci-github-actions-dev",
    },
    {
        "profile": "nbdb",
        "arn": "arn:aws:iam::691802122630:role/denaribot-deployment",
    },
]

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S%z"
