# vim: set fileencoding=utf-8 :

"""Unit Tests
"""

# Standard Library
from __future__ import absolute_import, division, print_function
import sys

# Third-party
try:
    import mock
except ImportError:
    import unittest.mock as mock

# Local/library specific
import kernel_cleanup


@mock.patch.object(sys, "argv", ["kernel_cleanup.py", "-n"])
def test_dryrun():
    # GIVEN
    # WHEN script is executed with dryrun
    kernel_cleanup.main()
    # THEN there are no exceptions
