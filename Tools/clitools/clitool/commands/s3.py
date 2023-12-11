import click
from click_shell import shell

from clitool.console import console
from clitool.services import S3Service, SessionService
from clitool.types.s3 import S3Bucket

session = SessionService()
s3 = S3Service(session)


# Validators ------------------------------------------------------------------
def validate(ctx, param, value: str | None = None) -> str:
    return value


# CLI commands ---------------------------------------------------------------
@shell("s3", prompt="AWS ❯ S3 ❯ ", intro="S3 commands.")
def cli():
    pass


@cli.command()
@click.option("--prefix", help="S3 bucket name prefix", type=str, default="")
def list_buckets(prefix: str):
    """List S3 buckets."""
    with console.status("Listing S3 bucket ...", spinner="dots"):
        try:
            buckets = s3.list_bucket(prefix)
        except Exception as e:
            console.log(f"Failed to get role: {e}", style="red")
            raise click.Abort()
        console.show_table([item.to_row() for item in buckets], S3Bucket.columns)
