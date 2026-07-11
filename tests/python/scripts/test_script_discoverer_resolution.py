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
import sys
import os
import unittest
import unittest.mock
import types

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
)

from scripts.scripts import ScriptDiscoverer
from scripts._internal.types import DiscoveryRegistry


class TestScriptDiscovererResolution(unittest.TestCase):
    @unittest.mock.patch("os.path.isdir")
    @unittest.mock.patch("os.listdir")
    @unittest.mock.patch("scripts.scripts.ScriptDiscoverer._load_module_from_path")
    def test_resolve_script_missing_metadata_constants_assigns_defaults(
        self,
        mock_load_module: unittest.mock.MagicMock,
        mock_listdir: unittest.mock.MagicMock,
        mock_isdir: unittest.mock.MagicMock,
    ) -> None:
        mock_isdir.return_value = True
        mock_listdir.return_value = ["empty_script.py"]

        mock_module: types.ModuleType = types.ModuleType("empty_script")

        mock_load_module.return_value = mock_module

        discoverer: ScriptDiscoverer = ScriptDiscoverer("some_path")
        registry: DiscoveryRegistry = discoverer.resolve_available_scripts()

        self.assertIn("empty_script.py", registry)
        self.assertEqual(
            registry["empty_script.py"]["who_am_i"], "No operational summary defined."
        )
        self.assertEqual(registry["empty_script.py"]["flags"], {})

    @unittest.mock.patch("os.path.isdir")
    @unittest.mock.patch("os.listdir")
    @unittest.mock.patch("scripts.scripts.ScriptDiscoverer._load_module_from_path")
    def test_resolve_script_with_malformed_flag_data_types(
        self,
        mock_load_module: unittest.mock.MagicMock,
        mock_listdir: unittest.mock.MagicMock,
        mock_isdir: unittest.mock.MagicMock,
    ) -> None:
        mock_isdir.return_value = True
        mock_listdir.return_value = ["broken_types.py"]

        mock_module: types.ModuleType = types.ModuleType("broken_types")
        mock_module.SCRIPT_BROKEN_TYPES_WHO_AM_I = "Test"  # type: ignore[attr-defined]
        mock_module.SCRIPT_BROKEN_TYPES_FLAGS = "this_should_be_a_dict_but_is_garbage"  # type: ignore[attr-defined]

        mock_load_module.return_value = mock_module

        discoverer: ScriptDiscoverer = ScriptDiscoverer("some_path")
        registry: DiscoveryRegistry = discoverer.resolve_available_scripts()

        self.assertEqual(
            registry["broken_types.py"]["flags"], "this_should_be_a_dict_but_is_garbage"
        )
