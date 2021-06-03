from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Protocol, Type

import boto3


@dataclass
class Credentials:
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_session_token: str | None = None
    aws_expiration: datetime | None = None
    aws_arn: str | None = None

    def serialize(self):
        return {
            "aws_access_key_id": self.aws_access_key_id,
            "aws_secret_access_key": self.aws_secret_access_key,
            "aws_session_token": self.aws_session_token,
            "aws_expiration": self.aws_expiration,
            "aws_arn": self.aws_arn,
        }

    @classmethod
    def deserialize(cls, data: dict) -> "Credentials":
        return cls(
            aws_arn=data.get("aws_arn"),
            aws_access_key_id=data.get("aws_access_key_id"),
            aws_secret_access_key=data.get("aws_secret_access_key"),
            aws_session_token=data.get("aws_session_token"),
            aws_expiration=data.get("aws_expiration"),
        )

    def is_expired(self):
        if self.aws_expiration is None:
            return False
        return self.aws_expiration < datetime.now(timezone.utc)


@dataclass
class Profile:
    credentials: Credentials
    name: str
    region: str
    user_id: str | None = None
    account: str | None = None
    arn: str | None = None

    columns = [
        {"header": "Name", "justify": "left"},
        {"header": "Region", "style": "yellow", "justify": "left"},
        {"header": "UserId", "style": "green", "justify": "center"},
        {"header": "Account", "style": "cyan", "justify": "center"},
        {"header": "Arn", "style": "violet", "justify": "left"},
    ]

    def to_row(self):
        return (
            f"[green]{self.name}[/green]",
            self.region,
            self.user_id,
            self.account,
            self.arn,
        )

    def serialize(self):
        return {
            "name": self.name,
            "region": self.region,
            "user_id": self.user_id,
            "account": self.account,
            "arn": self.arn,
            "credentials": self.credentials.serialize(),
        }

    @classmethod
    def deserialize(cls, data: dict) -> "Profile":
        return cls(
            name=data.get("name"),
            region=data.get("region"),
            user_id=data.get("user_id"),
            account=data.get("account"),
            arn=data.get("arn"),
            credentials=Credentials.deserialize(data.get("credentials")),
        )


# Session interface
class Session(Protocol):
    profile: Profile

    session: boto3.Session
    client: Type[boto3.client]
    resource: Type[boto3.resource]

    def get_profile(self, name: str, lazy=True) -> Profile:
        """Get an available profile by name."""

    def list_profiles(self) -> list[Profile]:
        """List all available profiles on your system."""

    def switch_profile(self, name: str) -> Profile:
        """Switch to a profile."""

    def set_credentials(self, credentials: Credentials) -> Profile:
        """Set credentials for a profile."""

    def assume_role(self, arn: str) -> Credentials:
        """Assume a IAM role."""

    def get_session_token(self, arn: str, mfa_token: str) -> Credentials:
        """Get a session token."""

    def store_aws_config_file(self, profile: Profile, name: str):
        """Store the profile in the AWS config file."""
