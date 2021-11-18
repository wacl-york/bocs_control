#!/usr/bin/env python
"""#############################################################################
Archives yesterday's log file.
================================================================================
#############################################################################"""
import argparse
import datetime
import glob
import logging
import os
import zipfile
import sys


# ===============================================================================

# ===============================================================================
def get_script_args():
    """
    Get command line arguments and options.

    Args:
        None.

    Returns:
        A argparse.Namespace object.
    """
    description = "Archives previous day's data file"
    arg_parser = argparse.ArgumentParser(description=description)
    help_string = "Path of directory in which to find data"
    arg_parser.add_argument(
        "data_directory", metavar="data_directory", type=str, help=help_string,
    )
    return arg_parser.parse_args()


def prepend_header(data_fn: str, header_fn: str) -> None:
    """
    Adds the header to the data file.

    Args:
        - data_fn (str): Filename containing the data log.
        - header_fn (str): Filename containing the header.

    Returns:
        None, saves the prepended file back to disk under the original filename
        (data_fn).
    """
    with open(data_fn, "r") as data_file:
        contents: list = data_file.readlines()

    try:
        with open(header_fn, "r") as header_file:
            header: list = header_file.readlines()
    except FileNotFoundError as ex:
        error_string = f"Couldn't open header file at {header_fn}"
        raise RuntimeError(error_string) from ex

    contents = header + contents

    with open(data_fn, "w") as data_file:
        data_file.writelines(contents)


def compress_file(filename: str) -> str:
    """
    Zip the file that we are going to transfer to S3.

    Args:
        - filename (str): File to be zipped.

    Returns:
        The resultant archive filename.
    """
    outfile_name = f"{filename}.zip"
    try:
        with zipfile.ZipFile(outfile_name, "w") as outzip:
            outzip.write(
                filename,
                compress_type=zipfile.ZIP_DEFLATED,
                arcname=os.path.basename(filename),
            )
    except zipfile.BadZipFile as ex:
        error_string = "Error when zipping file"
        raise RuntimeError(error_string) from ex

    return outfile_name


def file_to_archive(directory: str) -> str:
    """
    Get the file to be archived, looking for yesterday's date in the
    filename and a .log extension.

    Args:
        - directory (str): The directory where the log should be located.

    Returns:
        The filename of the log to be archived.
    """
    absolute_directory = os.path.abspath(directory)
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    date_string = yesterday.strftime("%Y-%m-%d")
    glob_pattern = os.path.join(absolute_directory, f"*{date_string}*.log")
    candidate = glob.glob(glob_pattern)

    if not candidate:
        error_string = f"Unable to find a data file matching yesterday's date ({date_string})"
        raise RuntimeError(error_string)

    if len(candidate) > 1:
        error_string = f"Multiple data files found for yesterday: {candidate}"
        raise RuntimeError(error_string)

    return candidate[0]


# ===============================================================================
def main():
    """
    Main entry point for this script.
    """
    script_args = get_script_args()

    try:
        logging.info(
            f"Attempting to archive yesterday's data file from directory {script_args.data_directory}"
        )
        data_file = file_to_archive(script_args.data_directory)
        prepend_header(data_file, "misc/header.txt")
        compress_file(data_file)
        os.remove(data_file)
    except RuntimeError as exception:
        logging.error(exception)
        logging.error("Terminating execution")
        ret_code = 1
    else:
        logging.info("Data log archived successfully.")
        ret_code = 0

    sys.exit(ret_code)


# ===============================================================================
if __name__ == "__main__":
    main()
