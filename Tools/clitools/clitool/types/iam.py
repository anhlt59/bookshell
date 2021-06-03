from dataclasses import dataclass

from clitool.types.session import Profile


@dataclass
class Role:
    arn: str
    profile: Profile

    columns = [
        {"header": "Profile", "style": "green", "justify": "left"},
        {"header": "Region", "style": "yellow", "justify": "left"},
        {"header": "Arn", "style": "cyan", "justify": "left"},
    ]

    def to_row(self):
        return self.profile.name, self.profile.region, self.arn

    def serialize(self):
        return {"arn": self.arn, "profile": self.profile.serialize()}

    @classmethod
    def deserialize(cls, data: dict) -> "Role":
        return cls(
            arn=data.get("arn"),
            profile=Profile.deserialize(data.get("profile")),
        )
