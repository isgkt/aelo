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
import io
import unittest

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
)

from scripts.scripts import DiscoveryPresenter
from scripts._internal.types import ScriptMetadata


class TestDiscoveryPresenter(unittest.TestCase):
    def setUp(self) -> None:
        self.held_output: io.StringIO = io.StringIO()
        sys.stdout = self.held_output

    def tearDown(self) -> None:
        sys.stdout = sys.__stdout__

    def test_display_explanation_with_zero_flags_registered(self) -> None:
        metadata: ScriptMetadata = {
            "who_am_i": "Minimal utility description",
            "flags": {},
        }

        DiscoveryPresenter.display_explanation("minimal.py", metadata)
        output: str = self.held_output.getvalue()

        self.assertIn(
            "No internal configurations or parameter flags registered.", output
        )

    def test_display_explanation_handles_malformed_and_extreme_unicode_flags(
        self,
    ) -> None:
        metadata: ScriptMetadata = {
            "who_am_i": "Unicode stress test",
            "flags": {
                "--💥-very-long-flag-parameter-that-exceeds-twenty-five-chars": (
                    "<🚨>",
                    "Explosion test",
                )
            },
        }

        DiscoveryPresenter.display_explanation("stress.py", metadata)
        output: str = self.held_output.getvalue()

        self.assertIn("Explosion test", output)
        self.assertIn(
            "--💥-very-long-flag-parameter-that-exceeds-twenty-five-chars <🚨>", output
        )
