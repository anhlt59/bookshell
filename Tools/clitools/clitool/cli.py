import click
from click_shell import shell
from rich import pretty, traceback

from clitool import commands
from clitool.cache import cache
from clitool.services import SessionService
from clitool.types.session import Profile


def cli_context_install(ctx: click.Context):
    session = SessionService()

    if profile_data := cache.get("profile"):
        profile = Profile.deserialize(profile_data)
        session.switch_profile(profile.name)
        # if credentials has been expired, refresh it
        if profile.credentials.is_expired():
            ctx.invoke(commands.session.refresh)
        else:
            session.set_credentials(profile.credentials)

    ctx.ensure_object(dict)
    ctx.obj["session"] = session
    return ctx


@shell(prompt="AWS ❯ ")
@click.option("--debug/--no-debug", default=False, required=False, help="Enable debug mode.")
@click.pass_context
def cli(ctx, debug):
    pretty.install()
    if debug:
        traceback.install()
    cli_context_install(ctx)

    @ctx.call_on_close
    def close():
        cache.set("profile", ctx.obj["session"].profile.serialize())
        cache.save()


def main():
    # build the command collection
    cli.add_command(commands.session)
    cli.add_command(commands.iam)
    cli.add_command(commands.s3)
    cli.add_command(commands.cloudformation)
    cli()


if __name__ == "__main__":
    main()
