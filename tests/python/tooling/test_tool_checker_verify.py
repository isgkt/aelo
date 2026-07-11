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

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
)

from scripts.tooling import ToolChecker, TOOL_TABLE


class TestToolCheckerVerify(unittest.TestCase):
    @unittest.mock.patch("shutil.which")
    @unittest.mock.patch("builtins.print")
    def test_verify_binary_missing_from_path(
        self, mock_print: unittest.mock.MagicMock, mock_which: unittest.mock.MagicMock
    ) -> None:
        mock_which.return_value = None

        checker: ToolChecker = ToolChecker("hyperfine")
        success: bool = checker.verify()

        self.assertFalse(success)
        mock_print.assert_called_once_with(
            "[ERROR] hyperfine target binary missing from PATH."
        )

    @unittest.mock.patch("shutil.which")
    @unittest.mock.patch("builtins.print")
    def test_verify_version_skipped_wildcard(
        self, mock_print: unittest.mock.MagicMock, mock_which: unittest.mock.MagicMock
    ) -> None:
        mock_which.return_value = "/usr/bin/cargo-mutants"

        checker: ToolChecker = ToolChecker("cargo-mutants")
        success: bool = checker.verify()

        self.assertTrue(success)
        mock_print.assert_called_once_with(
            "[OK] cargo-mutants located (version skipped)."
        )

    @unittest.mock.patch("shutil.which")
    @unittest.mock.patch("scripts.tooling.ToolChecker._get_first_line")
    @unittest.mock.patch("builtins.print")
    def test_verify_failed_to_extract_version_string(
        self,
        mock_print: unittest.mock.MagicMock,
        mock_get_line: unittest.mock.MagicMock,
        mock_which: unittest.mock.MagicMock,
    ) -> None:
        mock_which.return_value = "/usr/bin/lldb"
        mock_get_line.return_value = ""

        checker: ToolChecker = ToolChecker("lldb")
        success: bool = checker.verify()

        self.assertFalse(success)
        mock_print.assert_called_once_with(
            "[ERROR] Failed to extract version descriptor for lldb."
        )

    @unittest.mock.patch("shutil.which")
    @unittest.mock.patch("scripts.tooling.ToolChecker._get_first_line")
    @unittest.mock.patch("builtins.print")
    def test_verify_gnu_tool_strategy_success(
        self,
        mock_print: unittest.mock.MagicMock,
        mock_get_line: unittest.mock.MagicMock,
        mock_which: unittest.mock.MagicMock,
    ) -> None:
        mock_which.return_value = "/usr/bin/objdump"
        mock_get_line.return_value = "GNU objdump (GNU Binutils) 2.44"

        checker: ToolChecker = ToolChecker("objdump")
        success: bool = checker.verify()

        self.assertTrue(success)
        mock_print.assert_called_once_with("[OK] objdump 2.44")

    @unittest.mock.patch("shutil.which")
    @unittest.mock.patch("scripts.tooling.ToolChecker._get_first_line")
    @unittest.mock.patch("builtins.print")
    def test_verify_skip_words_strategy_success(
        self,
        mock_print: unittest.mock.MagicMock,
        mock_get_line: unittest.mock.MagicMock,
        mock_which: unittest.mock.MagicMock,
    ) -> None:
        mock_which.return_value = "/usr/bin/gh"
        mock_get_line.return_value = "gh version 2.46.0 (2024-03-01)"

        checker: ToolChecker = ToolChecker("gh")
        success: bool = checker.verify()

        self.assertTrue(success)
        mock_print.assert_called_once_with("[OK] gh 2.46.0")

    @unittest.mock.patch("shutil.which")
    @unittest.mock.patch("scripts.tooling.ToolChecker._get_first_line")
    @unittest.mock.patch("builtins.print")
    def test_verify_layout_constraint_violation(
        self,
        mock_print: unittest.mock.MagicMock,
        mock_get_line: unittest.mock.MagicMock,
        mock_which: unittest.mock.MagicMock,
    ) -> None:
        mock_which.return_value = "/usr/bin/python3"
        mock_get_line.return_value = (
            "Python"  # Faltam elementos para dar split no índice esperado
        )

        checker: ToolChecker = ToolChecker("python")
        success: bool = checker.verify()

        self.assertFalse(success)
        mock_print.assert_called_once_with(
            "[ERROR] Unexpected layout constraint for python: 'Python'"
        )

    @unittest.mock.patch("shutil.which")
    @unittest.mock.patch("scripts.tooling.ToolChecker._get_first_line")
    @unittest.mock.patch("builtins.print")
    def test_verify_version_mismatch_failure(
        self,
        mock_print: unittest.mock.MagicMock,
        mock_get_line: unittest.mock.MagicMock,
        mock_which: unittest.mock.MagicMock,
    ) -> None:
        mock_which.return_value = "/usr/bin/rustc"
        mock_get_line.return_value = "rustc 1.0.0 (old-version)"

        checker: ToolChecker = ToolChecker("rustc")
        success: bool = checker.verify()

        self.assertFalse(success)
        mock_print.assert_called_once_with(
            f"[FAIL] rustc - Expected: {TOOL_TABLE['rustc']}, Found: 1.0.0"
        )
