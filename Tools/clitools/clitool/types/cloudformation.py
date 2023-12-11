from dataclasses import dataclass
from datetime import datetime
from typing import Literal

from clitool.settings import DATETIME_FORMAT

CloudFormationStatus = Literal[
    "CREATE_IN_PROGRESS",
    "CREATE_FAILED",
    "CREATE_COMPLETE",
    "ROLLBACK_IN_PROGRESS",
    "ROLLBACK_FAILED",
    "ROLLBACK_COMPLETE",
    "DELETE_IN_PROGRESS",
    "DELETE_FAILED",
    "DELETE_COMPLETE",
    "UPDATE_IN_PROGRESS",
    "UPDATE_COMPLETE_CLEANUP_IN_PROGRESS",
    "UPDATE_COMPLETE",
    "UPDATE_FAILED",
    "UPDATE_ROLLBACK_IN_PROGRESS",
    "UPDATE_ROLLBACK_FAILED",
    "UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS",
    "UPDATE_ROLLBACK_COMPLETE",
    "REVIEW_IN_PROGRESS",
    "IMPORT_IN_PROGRESS",
    "IMPORT_COMPLETE",
    "IMPORT_ROLLBACK_IN_PROGRESS",
    "IMPORT_ROLLBACK_FAILED",
    "IMPORT_ROLLBACK_COMPLETE",
]


@dataclass
class CfnParameters:
    key: str
    value: str
    previous_value: str
    resolved_value: str


@dataclass
class CfnStack:
    name: str
    id: str | None = None
    status: CloudFormationStatus | None = None
    reason: str | None = None
    parameters: list[CfnParameters] | None = None
    role_arn: str | None = None
    # deletion_time: datetime | None = None
    creation_time: datetime | None = None
    last_updated_time: datetime | None = None

    columns = [
        {"header": "Id", "justify": "center", "style": "green"},
        {"header": "Name", "justify": "left", "style": "cyan"},
        {"header": "Status", "justify": "center", "style": "cyan1"},
        {"header": "Reason", "justify": "left", "style": "white"},
        {"header": "Parameters", "justify": "left", "style": "blue"},
        {"header": "LastUpdatedTime", "justify": "center", "style": "sky_blue2"},
        {"header": "CreationTime", "justify": "center", "style": "sky_blue1"},
        {"header": "RoleArn", "justify": "left"},
    ]

    def to_row(self):
        _id = self.id.split("/")[-1] if self.id else ""
        parameters = "\n".join([f"{param.key}: {param.value}" for param in self.parameters]) if self.parameters else ""
        last_updated_time = self.last_updated_time.strftime(DATETIME_FORMAT) if self.last_updated_time else ""
        creation_time = self.creation_time.strftime(DATETIME_FORMAT) if self.creation_time else ""
        return _id, self.name, self.status, self.reason, parameters, last_updated_time, creation_time, self.role_arn
