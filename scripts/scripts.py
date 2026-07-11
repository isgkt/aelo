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
import importlib.util
import os
import typing
import types
from scripts._internal.types import FlagManifest, DiscoveryRegistry, ScriptMetadata


class ScriptDiscoverer(object):
    """
    Handles dynamic scanning, isolation, and metadata reflection of internal
    repository pipeline scripts.
    """

    def __init__(self, directory: str) -> None:
        self.directory: str = os.path.abspath(directory)
        self.target_suffix: str = ".py"
        self.ignored_files: typing.Set[str] = {"scripts.py", "__init__.py"}

    def _load_module_from_path(
        self, module_name: str, file_path: str
    ) -> typing.Optional[types.ModuleType]:
        """
        Dynamically binds and injects a script file context into the Python runtime scope.
        """
        try:
            spec: typing.Optional[importlib.machinery.ModuleSpec] = (
                importlib.util.spec_from_file_location(module_name, file_path)
            )

            if spec is None or spec.loader is None:
                return None

            module: types.ModuleType = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            return module
        except Exception:
            return None

    def resolve_available_scripts(self) -> DiscoveryRegistry:
        """
        Scans the registered tracking directory to reflect automation signatures.
        """
        registry: DiscoveryRegistry = {}

        if not os.path.isdir(self.directory):
            return registry

        for filename in os.listdir(self.directory):
            if (
                not filename.endswith(self.target_suffix)
                or filename in self.ignored_files
            ):
                continue

            script_name: str = filename[: -len(self.target_suffix)]
            file_path: str = os.path.join(self.directory, filename)
            module: typing.Optional[types.ModuleType] = self._load_module_from_path(
                script_name, file_path
            )

            if module is None:
                continue

            token_prefix: str = f"SCRIPT_{script_name.upper()}"
            who_am_i: str = getattr(
                module, f"{token_prefix}_WHO_AM_I", "No operational summary defined."
            )
            flags: FlagManifest = getattr(module, f"{token_prefix}_FLAGS", {})
            registry[filename] = {"who_am_i": who_am_i, "flags": flags}

        return registry


class DiscoveryPresenter(object):
    """
    Formatters and displays systemic diagnostic schemas into readable standard output targets.
    """

    @staticmethod
    def display_list(registry: DiscoveryRegistry) -> None:
        """
        Renders an index of tracked repository helper utilities.
        """
        print("Registered executable scripts available:")
        for filename, metadata in sorted(registry.items()):
            print(f" - {filename}: {metadata['who_am_i']}")

    @staticmethod
    def display_explanation(filename: str, metadata: ScriptMetadata) -> None:
        """
        Outputs detailed usage profiles, design goals, and execution parameter constraints.
        """
        print(f"Script: {filename}")
        print(f"Description: {metadata['who_am_i']}\n")
        print("Available Flags / Options:")

        if not metadata["flags"]:
            print("  No internal configurations or parameter flags registered.")
            return

        for flag, design_data in sorted(metadata["flags"].items()):
            meta_argument, description = design_data
            parameter_signature: str = (
                f"{flag} {meta_argument}" if meta_argument else flag
            )
            print(f"  {parameter_signature.ljust(25)} : {description}")
