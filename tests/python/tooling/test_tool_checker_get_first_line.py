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
import subprocess

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
)

from scripts.tooling import ToolChecker


class TestToolCheckerGetFirstLine(unittest.TestCase):
    @unittest.mock.patch("subprocess.run")
    def test_get_first_line_happy_path_stdout(
        self, mock_run: unittest.mock.MagicMock
    ) -> None:
        mock_process: unittest.mock.MagicMock = unittest.mock.MagicMock()
        mock_process.stdout = "rustc 1.96.1 (c84f53e1b 2026-02-15)\n"
        mock_process.stderr = ""
        mock_run.return_value = mock_process

        checker: ToolChecker = ToolChecker("rustc")
        line: str = checker._get_first_line()

        self.assertEqual(line, "rustc 1.96.1 (c84f53e1b 2026-02-15)")
        mock_run.assert_called_once_with(
            ["rustc", "--version"], capture_output=True, text=True, check=True
        )

    @unittest.mock.patch("subprocess.run")
    def test_get_first_line_happy_path_stderr_fallback(
        self, mock_run: unittest.mock.MagicMock
    ) -> None:
        mock_process: unittest.mock.MagicMock = unittest.mock.MagicMock()
        mock_process.stdout = ""
        mock_process.stderr = 'java version "21.0.11" 2024-04-16 LTS\n'
        mock_run.return_value = mock_process

        checker: ToolChecker = ToolChecker("java")
        line: str = checker._get_first_line()

        self.assertEqual(line, 'java version "21.0.11" 2024-04-16 LTS')

    @unittest.mock.patch("subprocess.run")
    def test_get_first_line_command_failed(
        self, mock_run: unittest.mock.MagicMock
    ) -> None:
        mock_run.side_effect = subprocess.CalledProcessError(
            returncode=1, cmd=["gh", "--version"]
        )

        checker: ToolChecker = ToolChecker("gh")
        line: str = checker._get_first_line()

        self.assertEqual(line, "")

    @unittest.mock.patch("subprocess.run")
    def test_get_first_line_binary_not_found(
        self, mock_run: unittest.mock.MagicMock
    ) -> None:
        mock_run.side_effect = FileNotFoundError()

        checker: ToolChecker = ToolChecker("rr")
        line: str = checker._get_first_line()

        self.assertEqual(line, "")
