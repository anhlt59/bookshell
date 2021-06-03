from typing import Iterable

from clitool.services.base import AwsService
from clitool.settings import PROJECT_ROLES
from clitool.types.iam import Role


class IamService(AwsService):
    def list_project_roles(self, lazy=True) -> list[Role]:
        roles = []
        for item in PROJECT_ROLES:
            profile = self.session.get_profile(item.get("profile"), lazy=lazy)
            roles.append(Role(arn=item.get("arn"), profile=profile))
        return roles

    def get_project_role(self, arn: str, lazy=True) -> Role:
        roles = self.list_project_roles(lazy=lazy)
        for item in roles:
            if item.arn == arn:
                role = item
                break
        else:
            raise Exception(f"Role {arn} not found")
        return role

    def list_roles(self, **kwargs) -> Iterable[Role]:
        prefix = kwargs.pop("PathPrefix", None)
        response = self.session.client("iam").list_roles(**kwargs)

        for item in response.get("Roles", []):
            if not prefix or f"role/{prefix}" in item.get("Arn"):
                yield Role(
                    arn=item.get("Arn"),
                    profile=self.session.profile,
                )
        if response.get("IsTruncated"):
            kwargs.update(Marker=response.get("Marker"), PathPrefix=prefix)
            yield from self.list_roles(**kwargs)

    def list_policies(self, **kwargs) -> Iterable[Role]:
        response = self.session.client("iam").list_policies(**kwargs)

        for item in response.get("Policies", []):
            yield Role(arn=item.get("Arn"), profile=self.session.profile)
        if response.get("IsTruncated"):
            kwargs.update(Marker=response.get("Marker"))
            yield from self.list_policies(**kwargs)
