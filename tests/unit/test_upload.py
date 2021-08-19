"""#############################################################################
Unit tests for upload.py
================================================================================
#############################################################################"""
import os
import unittest
from unittest.mock import patch, Mock
import upload


class TestAddHeader(unittest.TestCase):
    def setUp(self):
        self.data_fn = "tmp_data.log"
        self.header_fn = "tmp_header.txt"
        self.assertFalse(os.path.exists(self.data_fn))
        self.assertFalse(os.path.exists(self.header_fn))

        self.dummy_data = ["1,2,3\n", "4,5,6\n"]
        self.dummy_header = "a,b,c\n"
        with open(self.data_fn, "w") as outfile:
            outfile.writelines(self.dummy_data)
        with open(self.header_fn, "w") as outfile:
            outfile.write(self.dummy_header)

    def tearDown(self):
        os.remove(self.data_fn)
        os.remove(self.header_fn)

    def test_success(self):
        upload.prepend_header(self.data_fn, self.header_fn)

        with open(self.data_fn, "r") as infile:
            new_content = infile.readlines()
        self.assertEqual(new_content, ["a,b,c\n", "1,2,3\n", "4,5,6\n"])
