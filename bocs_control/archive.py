"""
Archives yesterday's log file.

Adds the CSV header to yesterday's data log, compresses it with Zip, and removes
the original file.

Functions:

    prepend_header(str)
    compress_file(str) -> str
    get_file_to_archive() -> str
    main()

"""
import datetime
import glob
import logging
import os
import zipfile
import sys

import bocs_control.config as cfg


def prepend_header(data_fn: str) -> None:
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

    contents = cfg.HEADER + contents

    with open(data_fn, "w") as data_file:
        data_file.writelines(contents)


def compress_file(filename: str) -> str:
    """
    Zips the specified file.

    Args:
        - filename (str): File to be zipped.

    Returns:
        The resultant archive filename.

    Raises:
        RuntimeError
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


def get_file_to_archive() -> str:
    """
    Get the file to be archived, looking for yesterday's date in the
    filename and a .log extension.

    Args:
        - None.

    Returns:
        The filename of the log to be archived.

    Raises:
        RuntimeError
    """
    log_dir = cfg.DATA_LOG_DIR
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    date_string = yesterday.strftime("%Y-%m-%d")
    glob_pattern = os.path.join(log_dir, f"{date_string}_data.log")
    candidate = glob.glob(glob_pattern)

    if not candidate:
        error_string = f"Unable to find a data file matching yesterday's date ({date_string}) in dir {log_dir}"
        raise RuntimeError(error_string)

    if len(candidate) > 1:
        error_string = f"Multiple data files found for yesterday: {candidate} in dir {log_dir}"
        raise RuntimeError(error_string)

    return candidate[0]


def main():
    """
    Main entry point for this script.
    """
    try:
        logging.info(f"Attempting to archive yesterday's data file")
        data_file = get_file_to_archive()
        prepend_header(data_file)
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


if __name__ == "__main__":
    main()
