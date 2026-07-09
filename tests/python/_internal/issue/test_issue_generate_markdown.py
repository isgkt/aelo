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

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
)

from scripts._internal.issue import (
    Issue,
    IssueType,
)


class TestIssueGenerateMarkdown(unittest.TestCase):
    def test_generate_markdown_bug_happy_path(self) -> None:
        issue: Issue = Issue(IssueType.BugReport, "Title")

        issue.set_field("description", "Something broke")
        issue.set_field("environment-info", "OS: ReactOS")
        issue.set_field("compiler-output", "Exit code 139")

        markdown: str = issue._generate_markdown()
        expected: str = (
            "### Description & Visual Evidence\n\nSomething broke\n\n"
            "### Compiler Output or Error Reports\n\nExit code 139\n\n"
            "### Environment & System Information\n\nOS: ReactOS\n\n"
            "### Code Snippet or Reproduction Steps\n\n_No response_\n"
        )

        self.assertEqual(markdown, expected)

    def test_generate_markdown_bug_missing_required_field_description(self) -> None:
        issue: Issue = Issue(IssueType.BugReport, "Title")

        issue.set_field("environment-info", "OS: Linux")

        with self.assertRaises(ValueError) as context:
            issue._generate_markdown()

        self.assertIn("The required field 'description'", str(context.exception))

    def test_generate_markdown_bug_required_field_is_whitespace_only(self) -> None:
        issue: Issue = Issue(IssueType.BugReport, "Title")

        issue.set_field("description", "     \n   ")
        issue.set_field("environment-info", "OS: Linux")

        with self.assertRaises(ValueError) as context:
            issue._generate_markdown()

        self.assertIn("The required field 'description'", str(context.exception))

    def test_generate_markdown_feature_missing_required_field(self) -> None:
        issue: Issue = Issue(IssueType.FeatureRequest, "Title")

        issue.set_field("proposal-summary", "New feature idea")

        with self.assertRaises(ValueError) as context:
            issue._generate_markdown()

        self.assertIn(
            "The required field 'affected-components'", str(context.exception)
        )
