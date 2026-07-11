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
import subprocess
import shutil
import argparse
import sys

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

    def _get_first_line(self) -> str:
        """
        Executes the underlying binary requesting its version signature.
        """
        try:
            result: subprocess.CompletedProcess[str] = subprocess.run(
                [self.executable, "--version"],
                capture_output=True,
                text=True,
                check=True,
            )
            output: str = (
                result.stdout.strip() if result.stdout else result.stderr.strip()
            )

            return output.splitlines()[0] if output else ""
        except (subprocess.CalledProcessError, FileNotFoundError):
            return ""

    def verify(self) -> bool:
        """
        Evaluates the availability and structural constraints of the active tool.
        """
        if not shutil.which(self.executable):
            print(f"[ERROR] {self.tool} target binary missing from PATH.")
            return False

        if self.expected_version == "?":
            print(f"[OK] {self.tool} located (version skipped).")
            return True

        first_line: str = self._get_first_line()

        if not first_line:
            print(f"[ERROR] Failed to extract version descriptor for {self.tool}.")
            return False

        parts: typing.List[str] = first_line.split()
        found_version: str

        if self.tool in _GNU_TOOLS:
            found_version = parts[-1]
        elif self.tool in _SKIP_WORDS_REGISTRY:
            skip: int = _SKIP_WORDS_REGISTRY[self.tool]

            if len(parts) <= skip:
                print(
                    f"[ERROR] Unexpected layout constraint for {self.tool}: '{first_line}'"
                )
                return False

            found_version = parts[skip].lstrip("v")
        else:
            print(f"[ERROR] No parsing dispatch strategy defined for {self.tool}.")
            return False

        if found_version == self.expected_version:
            print(f"[OK] {self.tool} {found_version}")
            return True

        print(
            f"[FAIL] {self.tool} - Expected: {self.expected_version}, Found: {found_version}"
        )
        return False


def _parse_argument() -> argparse.Namespace:
    """
    Parses structural execution commands from standard system input vectors.
    """
    base_parser = argparse.ArgumentParser(description="Harpy Tooling Checker Pipeline")

    base_parser.add_argument(
        "--search",
        type=str,
        help="Checks whether a specific tool is available and matches target version schemas.",
    )
    base_parser.add_argument(
        "--all",
        action="store_true",
        help="Verify all registered environment toolkit manifests.",
    )
    base_parser.add_argument(
        "--list",
        action="store_true",
        help="List target specifications for registered tools.",
    )
    base_parser.add_argument(
        "--version",
        type=str,
        dest="get_version",
        help="Display the expected target version for a specific mapping.",
    )

    return base_parser.parse_args()


def main() -> None:
    """
    Execution gateway controlling flow dispatching based on parsed command line contexts.
    """
    arguments: argparse.Namespace = _parse_argument()

    if arguments.list:
        print("Registered baseline configurations:")

        for tool, version in TOOL_TABLE.items():
            print(f" - {tool}: {version}")

        return

    if arguments.get_version:
        if arguments.get_version in TOOL_TABLE:
            print(f"{arguments.get_version}: {TOOL_TABLE[arguments.get_version]}")
        else:
            sys.exit(1)

        return

    if arguments.search:
        try:
            checker: ToolChecker = ToolChecker(arguments.search)
            success: bool = checker.verify()

            if not success:
                sys.exit(1)
        except KeyError:
            sys.exit(1)

        return

    if arguments.all or len(sys.argv) == 1:
        global_success: bool = True

        for tool in TOOL_TABLE:
            try:
                if not ToolChecker(tool).verify():
                    global_success = False
            except KeyError:
                continue

        if not global_success:
            sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
    except Exception:
        sys.exit(1)
