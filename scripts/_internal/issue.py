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
import enum

_BUG_REPORT_LABELS: typing.List[str] = ["bug", "status: triage"]
_FEATURE_REQUEST_LABELS: typing.List[str] = ["feature", "status: triage"]
_BUG_FIELDS: typing.Dict[str, typing.Tuple[str, bool]] = {
    "description": ("Description & Visual Evidence", True),
    "compiler-output": ("Compiler Output or Error Reports", False),
    "environment-info": ("Environment & System Information", True),
    "reproduction": ("Code Snippet or Reproduction Steps", False),
}
_FEATURE_FIELDS: typing.Dict[str, typing.Tuple[str, bool]] = {
    "proposal-summary": ("Proposal Summary", True),
    "affected-components": ("Affected Components / Scope", True),
    "implementation-ideas": ("Implementation Details", False),
    "poc": ("Proof of Concept / Examples", False),
}


class IssueType(str, enum.Enum):
    """
    Specifies the classification category for GitHub repository issues.

    This enumeration guarantees strict alignment between the compiler's
    internal diagnostic pipelines and the predefined GitHub Issue Forms.
    """

    FeatureRequest = "Feature Request"
    BugReport = "Bug Report"
