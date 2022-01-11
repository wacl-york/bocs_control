"""
Unit tests for bocs_control.archive

Classes:

    TestAddHeader
"""
import os
import unittest
from unittest.mock import patch
from bocs_control import archive
from bocs_control.config import HEADER


class TestAddHeader(unittest.TestCase):
    """
    Unit tests for the prepend_header function.
    """

    def setUp(self):
        """
        Writes a dummy log file to disk.
        """
        self.data_fn = "tmp_data.log"
        self.assertFalse(os.path.exists(self.data_fn))

        self.dummy_data = ["1,2,3\n", "4,5,6\n"]
        self.dummy_header = ["a,b,c\n"]
        with open(self.data_fn, "w") as outfile:
            outfile.writelines(self.dummy_data)

    def tearDown(self):
        """
        Deletes the dummy log file.
        """
        os.remove(self.data_fn)

    def test_success(self):
        """
        Tests that the header is added to the log file.
        """
        with patch("bocs_control.archive.cfg.HEADER", self.dummy_header):
            archive.prepend_header(self.data_fn)

        with open(self.data_fn, "r") as infile:
            new_content = infile.readlines()
        self.assertEqual(new_content, ["a,b,c\n", "1,2,3\n", "4,5,6\n"])
