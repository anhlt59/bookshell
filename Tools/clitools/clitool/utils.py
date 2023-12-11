import re
from itertools import islice
from subprocess import PIPE, Popen
from typing import Any, Iterable

mfa_compiler = re.compile(r"(^arn:aws:iam::\d+:mfa/[\w\-_]+$)|(^\d{6,}$)")


def chunks(objs: Iterable[Any], limit: int) -> Iterable[list[Any]]:
    """
    Yield successive limit-sized chunks from a iterable.
    :param objs: list of any objects
    :param limit: chunk size
    :return: iterable limit-sized chunks
    """
    if isinstance(objs, list) or isinstance(objs, tuple):
        objs = iter(objs)
    while batch := list(islice(objs, limit)):
        yield batch


def execute_command(command: str, stdin=PIPE, stdout=PIPE):
    """
    Run a command and return the output.
    :param command: command to run
    :param stdin: standard input
    :param stdout: standard output
    :return: output of the command
    """
    args = command.split()
    with Popen(args, stdin=stdin, stdout=stdout, stderr=PIPE) as proc:
        stdout, stderr = proc.communicate()
        if proc.returncode != 0:
            raise Exception(f"COMMAND ERRROR: {stderr.decode('utf-8')}")
        return stdout
