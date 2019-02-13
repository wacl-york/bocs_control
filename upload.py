#!/usr/bin/env python
"""#############################################################################
AWS S3 Bucket Upload
================================================================================
This requires AWS credentials to be set up in the user home directory.
#############################################################################"""
import argparse
import os
import sys
#===============================================================================
import boto3
#===============================================================================
def get_script_args():
    """
    Get command line arguments and options.
    """
    description = 'Upload BOCS data to AWS S3 bucket'
    arg_parser = argparse.ArgumentParser(description=description)
    arg_parser.add_argument('site_name', metavar='site_name', nargs=1, type=str,
                            help='Name of remote monitoring site')
    help_string = 'Path of directory in which to find data to upload'
    arg_parser.add_argument('data_directory', metavar='data_directory', nargs=1,
                            type=str, help=help_string)
    return arg_parser.parse_args()

def file_to_upload(directory):
    """
    Get the second to last most recently modified file from directory, as this
    will be the file to upload.
    """
    absolute_directory = os.path.abspath(directory)
    directory_contents = [os.path.join(absolute_directory, filename)
                          for filename in os.listdir(absolute_directory)]
    directory_contents.sort(key=os.path.getmtime, reverse=True)

    return directory_contents[1]
#===============================================================================
def main():
    """
    Main entry point for this script.
    """
    script_args = get_script_args()

    profile_name = f'bocs-remote-uploads-{script_args.site_name[0]}'
    upfile_name = file_to_upload(script_args.data_directory[0])
    object_key = os.path.join(script_args.site_name[0],
                              os.path.basename(upfile_name))
    info_string = (f"INFO: UPLOADING {upfile_name} TO {object_key} IN BUCKET\n")
    sys.stderr.write(info_string)

    session = boto3.session.Session(profile_name=profile_name)
    s3 = session.resource('s3')

    s3.Bucket('bocs-remote-uploads').upload_file(upfile_name,
                                                 object_key)

    exit(0)
#===============================================================================
if __name__ == "__main__":
    main()
