import logging
import sys
from textwrap import dedent
from typing import NamedTuple, Self

from .osascript import call_osascript


logger = logging.getLogger(__name__)


class DisplaySet(NamedTuple):
    name: str
    active: bool = False

    @classmethod
    def list_display_sets(cls) -> list[Self]:
        """List all display sets."""
        display_set_names = _get_all_display_set_names()
        active_display_set_names = set(_get_active_display_set_names())
        display_sets = []
        for name in display_set_names:
            display_set = cls(
                name=name,
                active=name in active_display_set_names,
            )
            display_sets.append(display_set)
        return display_sets

    @property
    def name_and_activity_indicator(self) -> str:
        return f"{'*' if self.active else ' '} {self.name} "

    @classmethod
    def activate_display_set(cls, name: str) -> bool:
        logger.debug("Activating display set: %s", name)
        return _activate_display_set_(name)


def _get_all_display_set_names() -> list[str]:
    logger.debug("Getting all display set names")
    script = dedent(
        """
        on run
            set displaySetNames to {{}}
            tell application "SwitchResX Daemon"
                set displaySets to display sets
                repeat with displaySet in displaySets
                    set displaySetName to name of displaySet
                    copy displaySetName to end of displaySetNames
                end repeat
            end tell
            set AppleScript's text item delimiters to "\\n"
            return displaySetNames as string
        end run
        """
    )
    result = call_osascript(script)
    if result.returncode:
        logger.error("Error getting display set names: %s", result.stderr)
    names = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    logger.debug("Display set names: %s", names)
    return names


def _get_active_display_set_names() -> list[str]:
    logger.debug("Getting active display set names")
    script = dedent(
        """
        on run
            set displaySetNames to {{}}
            tell application "SwitchResX Daemon"
                set activeSets to current sets
                repeat with displaySet in activeSets
                    set displaySetName to name of displaySet
                    copy displaySetName to end of displaySetNames
                end repeat
            end tell
            set AppleScript's text item delimiters to "\\n"
            return displaySetNames as string
        end run
        """
    )
    result = call_osascript(script)
    if result.returncode:
        logger.error("Error getting active display set names: %s", result.stderr)
    names = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    logger.debug("Active display set names: %s", names)
    return names


def _activate_display_set_(display_set_name: str) -> bool:
    logger.debug("Activating display set: %s", display_set_name)
    script = dedent(
        f"""\
        on run
            set display_set_name to "{display_set_name}"
            tell application "SwitchResX Daemon"
                apply first display set of (display sets whose name = display_set_name)
            end tell
        end run
        """
    )
    result = call_osascript(script)
    if result.returncode:
        logger.error("Error activating display set: %s", result.stderr)
        sys.stderr.write(result.stderr)
        sys.stderr.write("\n")
        return False
    return True
