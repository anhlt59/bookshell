from dataclasses import dataclass
from datetime import datetime

from clitool.settings import DATETIME_FORMAT


@dataclass
class S3Bucket:
    name: str
    creation_date: datetime | None = None

    columns = [
        {"header": "Name", "style": "green", "justify": "left"},
        {"header": "CreationDate", "style": "yellow", "justify": "center"},
    ]

    def to_row(self):
        creation_date = self.creation_date.strftime(DATETIME_FORMAT) if self.creation_date else ""
        return self.name, creation_date

    def serialize(self):
        return {"name": self.name, "creation_date": self.creation_date}


@dataclass
class S3Object:
    key: str
    bucket: S3Bucket

    columns = [
        {"header": "Key", "style": "green", "justify": "center"},
        {"header": "Bucket", "style": "yellow", "justify": "center"},
    ]

    def to_row(self):
        return self.key, self.bucket.name

    def serialize(self):
        return {"key": self.key, "bucket": self.bucket.serialize()}
