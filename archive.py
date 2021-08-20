#!/usr/bin/env python
"""#############################################################################
Archives yesterday's log file.
================================================================================
#############################################################################"""
import argparse
import datetime
import glob
import gzip
import os
import sys

# ===============================================================================
import boto3

# ===============================================================================
def get_script_args():
    """
    Get command line arguments and options.
    """
    description = "Upload BOCS data to AWS S3 bucket"
    arg_parser = argparse.ArgumentParser(description=description)
    help_string = "Path of directory in which to find data"
    arg_parser.add_argument(
        "data_directory", metavar="data_directory", type=str, help=help_string,
    )
    return arg_parser.parse_args()


def prepend_header(data_fn: str, header_fn: str):
    """
    Adds the header to the data file.

    Args:
        - data_fn (str): Filename containing the data log.
        - header_fn (str): Filename containing the header.

    Returns:
        None, saves the prepended file back to disk under the original filename
        (data_fn).
    """
    with open(data_fn, "r+") as data_file:
        contents: list = data_file.readlines()
        with open(header_fn, "r") as header_file:
            header: str = header_file.read()
        data_file.seek(0, 0)
        data_file.write(header)
        data_file.writelines(contents)


def compress_file(filename):
    # TODO Change this to use zipfile module (standard library)
    """
    gzip the file that we are going to transfer to S3.
    """
    outfile_name = f"{filename}.gz"
    with open(filename, "rb") as infile, gzip.open(
        outfile_name, "wb"
    ) as outfile:
        outfile.writelines(infile)

    return outfile_name


def file_to_archive(directory):
    """
    Get the file to be archived, looking for yesterday's date in the
    filename and a .log extension.
    """
    absolute_directory = os.path.abspath(directory)
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    # As with comment in data_writer, this can probably be done more
    # interpretably with strftime('%Y-%m-%d')
    date_string = (
        f"{yesterday.year}-{str(yesterday.month).zfill(2)}-"
        f"{str(yesterday.day).zfill(2)}"
    )
    glob_pattern = os.path.join(absolute_directory, f"*{date_string}*.log")
    candidate = glob.glob(glob_pattern)

    if not candidate:
        error_string = "ERROR: UNABLE TO FIND YESTERDAY'S DATA FILE!\n"
        raise RuntimeError(error_string)

    if len(candidate) > 1:
        error_string = "ERROR: MULTIPLE DATA FILES FOUND FOR YESTERDAY!\n"
        raise RuntimeError(error_string)

    return candidate[0]


# ===============================================================================
def main():
    """
    Main entry point for this script.
    """
    script_args = get_script_args()

    try:
        data_file = file_to_archive(script_args.data_directory)
    except RuntimeError as exception:
        sys.stderr.write(str(exception))
        sys.exit(1)

    prepend_header(data_file, "misc/header.txt")

    compressed_data_file = compress_file(data_file)

    sys.exit(0)


# ===============================================================================
if __name__ == "__main__":
    main()
