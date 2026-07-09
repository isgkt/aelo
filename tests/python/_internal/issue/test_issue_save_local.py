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

from scripts._internal.issue import Issue, IssueType


class TestIssueSaveLocal(unittest.TestCase):
    @unittest.mock.patch("builtins.open", new_callable=unittest.mock.mock_open)
    def test_save_local_happy_path(self, mock_file: unittest.mock.MagicMock) -> None:
        issue: Issue = Issue(IssueType.BugReport, "Local Save Bug")

        issue.set_field("description", "A description")
        issue.set_field("environment-info", "A environment")
        issue.save_local("dummy_path.md")

        mock_file.assert_called_once_with("dummy_path.md", "w", encoding="utf-8")

        handle: unittest.mock.MagicMock = mock_file()
        written_content: str = "".join(
            call.args[0] for call in handle.write.call_args_list
        )

        self.assertIn("Title: Local Save Bug", written_content)
        self.assertIn("Labels: bug, status: triage", written_content)
        self.assertIn("### Description & Visual Evidence", written_content)

    def test_save_local_validation_failure_does_not_write_file(self) -> None:
        issue: Issue = Issue(IssueType.BugReport, "Validation Fail")

        with unittest.mock.patch(
            "builtins.open", unittest.mock.mock_open()
        ) as mock_file:
            with self.assertRaises(ValueError):
                issue.save_local("should_not_exist.md")
            mock_file.assert_not_called()
