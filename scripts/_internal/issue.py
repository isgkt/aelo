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


class Issue(object):
    """
    Represents a structured GitHub issue matching the repository form
    templates.

    The state of an issue encapsulates its metadata and a dictionary of fields
    mapped directly from the target form layout schema.
    """

    def __init__(self, issue_type: IssueType, title: str) -> None:
        """
        Initializes a new issue container with a distinct layout configuration.

        Based on the `issue_type`, this constructor assigns the appropriate
        labels and extracts the schema mapping that governs which tracking
        fields are expected.

        # Errors

        - **ValueError:** Raised if the provided `title` is empty or contains only whitespace characters.
        """
        self.issue_type: IssueType = issue_type

        if not title.strip():
            raise ValueError("The issue title cannot be blank.")

        self.title: str = title

        if self.issue_type == IssueType.BugReport:
            self.labels: typing.List[str] = _BUG_REPORT_LABELS.copy()
            self._expected_fields = _BUG_FIELDS
        else:
            self.labels = _FEATURE_REQUEST_LABELS.copy()
            self._expected_fields = _FEATURE_FIELDS

        self.fields: typing.Dict[str, str] = {}

    def set_field(self, field_identifier: str, value: str) -> None:
        """
        Binds a sanitized text payload to a specific issue form field.

        The value is trimmed of leading and trailing whitespaces before
        assignment.

        # Errors

        - **KeyError:** Raised if the `field_identifier` does not exist within the allowed fields definition for the active `IssueType`.
        """
        if field_identifier not in self._expected_fields:
            raise KeyError(
                f"The '{field_identifier}' field is invalid for the {self.issue_type.value} type. "
                f"Allowed fields: {list(self._expected_fields.keys())}"
            )

        self.fields[field_identifier] = value.strip()

    def _generate_markdown(self) -> str:
        """
        Compiles the localized fields into a standardized GitHub Markdown body.

        The compiler iterates through the expected form layout sequentially to
        guarantee the visual hierarchy remains unchanged when rendered
        upstream.

        # Post-Processing & Fallbacks

        - **Optional Fields:** If an optional field is missing or evaluated as empty, the string `_No response_` is explicitly injected as the default placeholder.

        # Errors

        - **ValueError:** Raised if any field designated as mandatory has not been set or contains an empty string.
        """
        lines: typing.List[str] = []

        for field_identifier, (label, is_required) in self._expected_fields.items():
            value: str = self.fields.get(field_identifier, "").strip()

            if is_required and not value:
                raise ValueError(
                    f"The required field '{field_identifier}' ({label}) has not been filled in."
                )

            if not value:
                value = "_No response_"

            lines.append(f"### {label}")
            lines.append("")
            lines.append(value)
            lines.append("")

        return "\n".join(lines)

    def save_local(self, filepath: str) -> None:
        """
        Serializes and commits the issue manifest directly to a local file
        path.

        This acts as a fallback mechanism allowing users to export drafts
        offline.

        # Side Effects

        - Performs disk I/O operations by opening and writing text encoded in UTF-8.
        - Emits a diagnostic status report to `stdout`.

        # Errors

        - **ValueError:** Propagated from `_generate_markdown` if strict layout validation rules are violated.
        """
        body_content: str = self._generate_markdown()
        content: str = (
            f"Title: {self.title}\nLabels: {', '.join(self.labels)}\n\n{body_content}"
        )

        with open(filepath, "w", encoding="utf-8") as file_path:
            file_path.write(content)

        print(f"Issue draft saved at: {filepath}")
