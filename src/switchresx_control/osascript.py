import logging
import subprocess
from textwrap import indent
from typing import NamedTuple


logger = logging.getLogger(__name__)


class ProcResult(NamedTuple):
    returncode: int
    stdout: str
    stderr: str


def call_osascript(script: str) -> ProcResult:
    """Call osascript to run some script."""
    logger.debug("Calling osascript to run:\n%s", indent(script, "    "))
    proc = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True,
        encoding="utf-8",
        timeout=5,
    )
    logger.debug("osascript stdout:")
    logger.debug(proc.stdout)
    logger.debug("osascript stderr:")
    logger.debug(proc.stderr)
    return ProcResult(
        returncode=proc.returncode,
        stdout=proc.stdout,
        stderr=proc.stderr,
    )
