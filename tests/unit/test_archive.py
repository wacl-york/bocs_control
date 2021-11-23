"""#############################################################################
Unit tests for archive.py
================================================================================
#############################################################################"""
import os
import unittest
from unittest.mock import patch, Mock
from bocs_control import archive
from bocs_control.header import HEADER


class TestAddHeader(unittest.TestCase):
    def setUp(self):
        self.data_fn = "tmp_data.log"
        self.assertFalse(os.path.exists(self.data_fn))

        self.dummy_data = ["1,2,3\n", "4,5,6\n"]
        self.dummy_header = ["a,b,c\n"]
        with open(self.data_fn, "w") as outfile:
            outfile.writelines(self.dummy_data)

    def tearDown(self):
        os.remove(self.data_fn)

    def test_success(self):
        with patch("bocs_control.archive.HEADER", self.dummy_header):
            archive.prepend_header(self.data_fn)

        with open(self.data_fn, "r") as infile:
            new_content = infile.readlines()
        self.assertEqual(new_content, ["a,b,c\n", "1,2,3\n", "4,5,6\n"])
