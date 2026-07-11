#     )
#  ( /(                                   (           (
#  )\())    )  (           (              )\       (  )\
# ((_)\  ( /(  )(   `  )   )\ )     __ ((((_)(    ))\((_) (
#  _((_) )(_))(()\  /(/(  (()/(    / /  )\ _ )\  /((_)_   )\
# | || |((_)_  ((_)((_)_\  )(_))  / /   (_)_\(_)(_)) | | ((_)
# | __ |/ _` || '_|| '_ \)| || | /_/     / _ \  / -_)| |/ _ \
# |_||_|\__,_||_|  | .__/  \_, |        /_/ \_\ \___||_|\___/
#                  |_|     |__/
#
# Copyright 2026 Ismael Moreira
#
# This file is distributed under the BSD 3-Clause License.
#
# See the LICENSE.txt file for more information.
import typing

TOOL_TABLE: typing.Dict[str, str] = {
    "python": "3.13.5",
    "rustc": "1.96.1",
    "cargo": "1.96.1",
    "cargo-fuzz": "0.13.2",
    "cargo-criterion": "1.1.0",
    "cargo-tarpaulin": "0.37.0",
    "cargo-mutants": "?",
    "gh": "2.46.0",
    "hyperfine": "1.19.0",
    "lldb": "19.1.7",
    "rr": "5.9.0",
    "objdump": "2.44",
    "readelf": "2.44",
    "nm": "2.44",
    "java": "21.0.11",
    "pyghidraRun": "?",
    "strace": "6.13",
    "ltrace": "0.7.91",
}
_SKIP_WORDS_REGISTRY: typing.Dict[str, int] = {
    "python": 1,
    "rustc": 1,
    "cargo": 1,
    "cargo-fuzz": 1,
    "cargo-criterion": 1,
    "cargo-tarpaulin": 1,
    "hyperfine": 1,
    "java": 1,
    "ltrace": 1,
    "gh": 2,
    "lldb": 2,
    "rr": 2,
    "strace": 3,
}
_GNU_TOOLS: typing.Set[str] = {"objdump", "readelf", "nm"}


class ToolChecker(object):
    """
    Provides validation services for host system binary executables and their
    respective structural versions.
    """

    def __init__(self, tool: str) -> None:
        """
        Initializes the context container for a targeted environment tool.

        # Errors

        - **KeyError:** Raised if the requested `tool` is missing from the global `TOOL_TABLE`.
        """
        if tool not in TOOL_TABLE:
            print(
                f"[Error] The tool '{tool}' is not recognized or tracked by this repository."
            )
            raise KeyError

        self.tool: str = tool
        self.expected_version: str = TOOL_TABLE[tool]
        self.executable: str = "python3" if tool == "python" else tool
