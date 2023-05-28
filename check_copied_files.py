#!/usr/bin/env python3

"""
A script to generate checksums for files in a source directory and verify 
them against files in a destination directory.
"""

# Necessary modules are imported
import argparse
import hashlib
import glob
import os
from tqdm import tqdm

# This function generates a checksum for a given file using the specified 
# algorithm
def generate_checksum(file_path, checksum_extension, algorithm):
    """
    Generates a checksum for a file.

    Args:
        file_path: The path to the file.
        checksum_extension: The extension to use for the checksum file.
        algorithm: The hashing algorithm to use.

    Returns:
        The path to the checksum file.
    """

    # File is read in binary mode
    with open(file_path, 'rb') as f:
        # All bytes from the file are read
        bytes = f.read()
        # The hash is calculated
        readable_hash = getattr(hashlib, algorithm)(bytes).hexdigest()

        # The checksum file path is created and the checksum is written to 
        # the file
        checksum_file_path = f'{file_path}.{checksum_extension}'
        with open(checksum_file_path, 'w') as cf:
            cf.write(readable_hash)
        return checksum_file_path

# This function validates the checksum of a given file against a stored checksum
def validate_checksum(file_path, checksum_file_path, algorithm):
    """
    Validates a file against a checksum.

    Args:
        file_path: The path to the file.
        checksum_file_path: The path to the checksum file.
        algorithm: The hashing algorithm to use.

    Returns:
        True if the file's checksum matches the stored checksum, 
        False otherwise.
    """

    # The file and the stored checksum are read
    with open(file_path, 'rb') as f:
        bytes = f.read() 
        readable_hash = getattr(hashlib, algorithm)(bytes).hexdigest()

    with open(checksum_file_path, 'r') as cf:
        stored_hash = cf.read()

    # The calculated checksum and the stored checksum are compared
    return stored_hash == readable_hash

# The main function that coordinates the script's operations
def main():
    """
    Main function to parse command line arguments and run the script.
    """

    # Command line arguments are parsed
    parser = argparse.ArgumentParser(
        description='This tool generates checksums for files in a source '
                    'directory and compares them against files in a '
                    'destination directory. If a destination directory is not '
                    'provided, the tool only generates checksums in the source '
                    'directory.')

    parser.add_argument('-s', '--source', required=True, 
                        help='Path to the source directory.')

    parser.add_argument('-d', '--destination',
                        help='Path to the destination directory (optional). If '
                             'not provided, the tool only generates checksums '
                             'without checking any files.')

    parser.add_argument('-f', '--filter', default='*', 
                        help='File name filter (optional). By default, all '
                             'files are processed. Checksum files are always '
                             'excluded.')

    parser.add_argument('-e', '--extension', default='checksum', 
                        help='Extension for the checksum files (optional). By '
                             'default, the extension is "checksum".')

    parser.add_argument('-a', '--algorithm', default='md5', 
                        choices=hashlib.algorithms_guaranteed,
                        help='Checksum algorithm (optional). By default, the '
                             'MD5 algorithm is used. You can specify any '
                             'algorithm guaranteed to be supported by Python\'s '
                             'hashlib module. The list of such algorithms can '
                             'be found in the hashlib module documentation.')

    parser.add_argument('-c', '--force-check', action='store_true',
                        help='Force checking files against checksum in the source '
                             'folder if checksum file exists for that file.')

    args = parser.parse_args()

    # All files in the source directory that match the filter and are not 
    # checksum files are identified
    source_files = []
    for dirpath, dirnames, filenames in os.walk(args.source):
        for filename in filenames:
            if not filename.endswith(args.extension):
                source_files.append(os.path.join(dirpath, filename))
    
    # For each file in the source directory...
    for file_path in tqdm(source_files, desc="Processing files", unit="file"):
        relative_path = os.path.relpath(file_path, args.source)
        checksum_file_path = f'{file_path}.{args.extension}'

        # If a checksum file doesn't exist, it is created
        if not os.path.exists(checksum_file_path):
            print(f'Checksum file does not exist for {file_path}. '
                  f'Creating it...')
            checksum_file_path = generate_checksum(file_path, 
                                                   args.extension,
                                                   args.algorithm)

        # If the force check option is enabled, the file is checked against 
        # the checksum
        if args.force_check:
            print(f'Checking file {file_path} in the source folder...')
            if validate_checksum(file_path, checksum_file_path, args.algorithm):
                print(f'Checksum matches for {file_path}.')
            else:
                print(f'WARNING!!! Checksum does not match for {file_path}.')

        # If a destination directory is provided, the file is checked against 
        # the checksum in the destination directory
        if args.destination:
            destination_file_path = os.path.join(args.destination, 
                                                 relative_path)
            if os.path.exists(destination_file_path):
                print(f'Checking file {destination_file_path}...')
                if validate_checksum(destination_file_path, 
                                     checksum_file_path,
                                     args.algorithm):
                    print(f'Checksum matches for {destination_file_path}.')
                else:
                    print(f'WARNING!!! Checksum does not match for '
                          f'{destination_file_path}.')

# If the script is run directly (and not imported as a module), the main 
# function is called
if __name__ == "__main__":
    main()
