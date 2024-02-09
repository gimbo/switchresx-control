"""Some script."""

import logging
import sys

from rich import pretty, print, traceback
from rich.logging import RichHandler

from switchresx_control.display_set import DisplaySet
from switchresx_control.utils.argparse import ArgumentParser, unpack_args


logger = logging.getLogger(__name__)
pretty.install()
traceback.install(show_locals=True)


def main():
    args = parse_args()
    logging.basicConfig(
        level="DEBUG" if args.debug else "INFO",
        format="%(message)s",
        datefmt="%Y-%m-%d%H:%M:%S+%z",
        handlers=[RichHandler()],
    )
    logger.debug("Args: %s", args)
    args.func(args)


@unpack_args
def cmd_list(focus: bool | None):
    """List display set names"""
    display_sets = DisplaySet.list_display_sets()
    display_sets = (
        display_sets
        if focus is None
        else [ds for ds in display_sets if ds.active == focus]
    )
    print("\n".join(ds.name_and_activity_indicator for ds in display_sets))


@unpack_args
def cmd_activate(name: str):
    """Activate a display set"""
    result = DisplaySet.activate_display_set(name)
    if not result:
        print(f"Failed to activate display set: {name}")


def parse_args(args_raw: tuple[str, ...] = tuple(sys.argv[1:])):
    parser = ArgumentParser(
        description=__doc__,
    )
    parser.add_debug_argument()

    cmd_parsers = parser.add_subparsers(
        dest="command",
        metavar="COMMAND",
        required=True,
        help="Command to execute; each has its own args and --help",
    )
    cmd_list_parser = cmd_parsers.add_parser(
        "list",
        aliases=["l"],
        description=cmd_list.__doc__,
    )
    cmd_list_parser.add_boolean_switch_group(
        "a",
        "active",
        "List only active display sets (default is to list all)",
        "i",
        "inactive",
        "List only inactive display sets (default is to list all)",
        dest="focus",
        default=None,
    )
    cmd_list_parser.set_defaults(func=cmd_list)

    cmd_activate_parser = cmd_parsers.add_parser(
        "activate",
        aliases=["a"],
        description=cmd_activate.__doc__,
    )
    cmd_activate_parser.add_argument(
        "name",
        help="Name of display set to activate",
    )
    cmd_activate_parser.set_defaults(func=cmd_activate)

    return parser.parse_args(args_raw)
