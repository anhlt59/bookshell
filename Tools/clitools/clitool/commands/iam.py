import click
from click_shell import shell

from clitool.cache import cache
from clitool.console import console
from clitool.services import IamService, SessionService
from clitool.settings import AWS_DEFAULT_SESSION_PROFILE
from clitool.types.iam import Role
from clitool.utils import mfa_compiler

session = SessionService()
iam = IamService(session)


# Validators ------------------------------------------------------------------
def validate_project_role(ctx, param, arn: str | None = None) -> str:
    available_roles = iam.list_project_roles()
    role_arns = [role.arn for role in available_roles]

    # if value is not None, check if it exists in the list of roles
    # else try to get the default role from cache
    if arn is None:
        if cached_role := ctx.obj.get("role"):
            return validate_project_role(ctx, param, cached_role.arn)
    elif arn in role_arns:
        return arn
    else:
        console.clear()
        console.log(f"RoleArn(arn={arn}) not found", style="yellow")

    # if cache is empty or role is not found, prompt the user to choose a role
    console.show_table([item.to_row() for item in available_roles], Role.columns)
    arn = click.prompt("Please choice a role arn")
    return validate_project_role(ctx, param, arn)


# CLI commands ---------------------------------------------------------------
@shell("iam", prompt="AWS ❯ IAM ❯ ")
def cli():
    pass


@shell("role", prompt="AWS ❯ IAM ❯ Role ❯ ")
def iam_role():
    pass


@shell("policy", prompt="AWS ❯ IAM ❯ Policy ❯ ")
def iam_policy():
    pass


cli.add_command(iam_role)
cli.add_command(iam_policy)


@iam_role.command()
@click.option("--arn", callback=validate_project_role, help="Role ARN")
def assume(arn):
    """Assume a IAM role."""
    with console.status(f"Switching to [b][cyan]{arn}[/cyan][/b] profile ...", spinner="dots") as status:
        try:
            role = iam.get_project_role(arn)
            session.switch_profile(role.profile.name)
            if mfa_compiler.match(role.arn):
                # prompt for MFA token
                status.stop()
                mfa_token = click.prompt("Please enter MFA token")
                status.start()
                credentials = session.get_session_token(role.arn, mfa_token)
            else:
                credentials = session.assume_role(arn=role.arn)
            profile = session.set_credentials(credentials)
        except Exception as e:
            console.log(f"Failed to get role: {e}", style="red")
            raise click.Abort()

    cache.set("profile", session.profile.serialize())
    console.log(f"Assumed role [b]{arn}[/b] successfully", style="green")
    session.store_aws_config_file(profile, AWS_DEFAULT_SESSION_PROFILE)
    console.log(f"Profile [b]{AWS_DEFAULT_SESSION_PROFILE}[/b] stored in ~/.aws/credentials", style="yellow")


@iam_role.command("list")
def _list():
    """List all available IAM roles configured in the setttings file."""
    with console.status("Listing project roles ...", spinner="dots"):
        roles = iam.list_project_roles()
        console.show_table([item.to_row() for item in roles], Role.columns)


@iam_role.command()
@click.option("--arn", callback=validate_project_role, help="Role ARN")
def get(arn: str):
    """Get a IAM role."""
    with console.status("Get role [b][cyan]{arn}[/cyan][/b]...", spinner="dots"):
        role = iam.get_project_role(arn, lazy=False)
        console.show_table([role.to_row()], Role.columns)
