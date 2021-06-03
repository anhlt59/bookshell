import time

import click
from click_shell import shell

from clitool.console import console
from clitool.services import CloudFormationService, SessionService
from clitool.types.cloudformation import CfnStack

session = SessionService()
cloudformation = CloudFormationService(session)


# Validators ------------------------------------------------------------------
def validate_name(ctx=None, param=None, name=None) -> str:
    stacks = cloudformation.list_stacks()
    available_names = [stack.name for stack in stacks]

    if name:
        if name in available_names:
            return name
        else:
            console.clear()
            console.log(f"CfnStack(name='{name}') not found", style="yellow")

    console.show_table([item.to_row() for item in stacks], CfnStack.columns)
    name = click.prompt("Please choice a stack name")
    return validate_name(ctx, param, name)


# CLI commands ---------------------------------------------------------------
@shell("cfn", prompt="AWS ❯ CloudFormation ❯ ")
def cli():
    pass


@cli.command("list")
@click.option("--prefix", help="Stack prefix", type=str, default=None)
def _list(prefix: str):
    """List cloudformation stacks."""
    with console.status("Listing cloudformation stack ...", spinner="dots"):
        try:
            stacks = cloudformation.list_stacks(prefix=prefix)
        except Exception as e:
            console.log(f"Failed to get stack: {e}", style="red")
            raise click.Abort()
        console.show_table([item.to_row() for item in stacks], CfnStack.columns)


@cli.command()
@click.option("--name", help="Stack name", callback=validate_name)
def get(name: str):
    """Describe a cloudformation stack."""
    with console.status(f"Getting [b][cyan]{name}[/cyan][/b] stack ...", spinner="dots"):
        try:
            stack = cloudformation.describle_stack(name)
        except Exception as e:
            console.log(f"Failed to get stack: {e}", style="red")
            raise click.Abort()
        console.show_table([stack.to_row()], CfnStack.columns)


@cli.command()
@click.option("--name", help="Stack name", callback=validate_name)
@click.option("--timeout", help="Monitoring timeout", type=int, default=300)
def monitor(name: str, timeout: int):
    """Monitor a cloudformation stack."""

    def generate(_name: str, _timeout: int):
        while _timeout > 0:
            stack = cloudformation.describle_stack(_name).to_row()
            yield [stack]
            time.sleep(1)
            _timeout -= 1
        raise click.Abort("Timed out!!!")

    with console.status(
        f"Monitoring [b][cyan]{name}[/cyan][/b] stack ...\n[white]Press Ctrl+C to stop[/white]", spinner="dots"
    ):
        try:
            console.live_table(generate(name, timeout), CfnStack.columns, refresh_per_second=0.2)
        except KeyboardInterrupt:
            console.log("Stopped monitoring stack", style="yellow")
            raise click.Abort()
        except Exception as e:
            console.log(f"Failed to get stack: {e}", style="red")
            raise click.Abort()
