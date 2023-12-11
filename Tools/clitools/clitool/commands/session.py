import click
from click_shell import shell

from clitool.console import console
from clitool.services import SessionService
from clitool.settings import AWS_DEFAULT_SESSION_PROFILE
from clitool.types.session import Profile
from clitool.utils import mfa_compiler

session = SessionService()


# Validators ------------------------------------------------------------------
def validate_profile(ctx=None, param=None, name=None) -> str:
    profiles = session.list_profiles()
    profile_names = [profile.name for profile in profiles]

    # if profile_name is not None, check if it exists in the list of profiles
    # else try to get the profile from cache
    if name is None:
        if cached_profile := ctx.obj.get("profile"):
            return validate_profile(ctx, param, cached_profile.arn)
    elif name in profile_names:
        return name
    else:
        console.clear()
        console.log(f"Profile(name='{name}') not found", style="yellow")

    # if cache is empty or profile is not found, prompt the user to choose a profile
    console.show_table([item.to_row() for item in profiles], Profile.columns)
    name = click.prompt("Please choice a profile name")
    return validate_profile(ctx, param, name)


# CLI commands ---------------------------------------------------------------
@shell("session", prompt="AWS ❯ Session ❯ ")
def cli():
    pass


@cli.command("list", help="List all available profiles on your system.")
def _list():
    """List all available profiles on your system."""
    with console.status("Listing profiles ...", spinner="dots"):
        profiles = session.list_profiles()
        console.show_table([profile.to_row() for profile in profiles], Profile.columns)


@cli.command(help="Get current profile.")
def current():
    """Get a profile."""
    with console.status("Get current profile ...", spinner="dots"):
        console.show_table([session.profile.to_row()], Profile.columns)


@cli.command(help="Get a profile by name.")
@click.option("--name", callback=validate_profile)
def get(name):
    """Get a profile."""
    with console.status(f"Get [b][cyan]{name}[/cyan][/b] profile...", spinner="dots"):
        try:
            profile = session.get_profile(name, False)
        except Exception as e:
            console.log(f"Profile {name} is inactive: {e}", style="red")
        else:
            console.show_table([profile.to_row()], Profile.columns)


@cli.command(help="Switch to a profile.")
@click.option("--name", callback=validate_profile)
def switch(name: str):
    """Switch to a profile."""
    if session.profile.name == name:
        console.log(f"Already in {name} profile", style="yellow")
        raise click.Abort()

    with console.status(f"Switching to [b][cyan]{name}[/cyan][/b] profile ...", spinner="dots"):
        try:
            profile = session.switch_profile(name)
        except Exception as e:
            console.log(f"Failed to switch {name} profile: {e}", style="red")
            raise click.Abort()

    console.log(f"Switched to {profile}", style="green")
    session.store_aws_config_file(profile, AWS_DEFAULT_SESSION_PROFILE)
    console.log(f"Profile [b]{AWS_DEFAULT_SESSION_PROFILE}[/b] stored in ~/.aws/credentials", style="yellow")


@cli.command(help="Refresh the session token.")
def refresh():
    """Refresh the session token."""
    credentials = session.profile.credentials
    if credentials.aws_expiration is None:
        console.log("Permanent credentials, no need to refresh", style="yellow")
        raise click.Abort()

    with console.status("Refreshing session token ...", spinner="dots") as status:
        try:
            if mfa_compiler.match(credentials.aws_arn):
                status.stop()
                mfa_token = click.prompt("Please enter MFA token")
                status.start()
                credentials = session.get_session_token(credentials.aws_arn, mfa_token)
            else:
                credentials = session.assume_role(credentials.aws_arn)
        except Exception as e:
            console.log(f"Failed to refresh session token: {e}", style="red")
            raise click.Abort()

        session.set_credentials(credentials)
        session.store_aws_config_file(session.profile, AWS_DEFAULT_SESSION_PROFILE)
        console.log(f"Profile [b]{AWS_DEFAULT_SESSION_PROFILE}[/b] has been refreshed", style="yellow")
