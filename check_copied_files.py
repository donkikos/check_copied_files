#!/usr/bin/env python3

"""
A script to generate checksums for files in a source directory and verify 
them against files in a destination directory.
"""

import argparse
import hashlib
import glob
import os
from tqdm import tqdm

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
    with open(file_path, 'rb') as f:
        bytes = f.read()
        readable_hash = getattr(hashlib, algorithm)(bytes).hexdigest()
        checksum_file_path = f'{file_path}.{checksum_extension}'
        with open(checksum_file_path, 'w') as cf:
            cf.write(readable_hash)
        return checksum_file_path

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
    with open(file_path, 'rb') as f:
        bytes = f.read() 
        readable_hash = getattr(hashlib, algorithm)(bytes).hexdigest()

    with open(checksum_file_path, 'r') as cf:
        stored_hash = cf.read()

    return stored_hash == readable_hash

def main():
    """
    Main function to parse command line arguments and run the script.
    """
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

    args = parser.parse_args()

    source_files = [f for f in glob.glob(os.path.join(args.source, 
                                                      '**', 
                                                      args.filter), 
                                         recursive=True) 
                    if os.path.isfile(f) and not f.endswith(args.extension)]

    for file_path in tqdm(source_files, desc="Processing files", unit="file"):
        relative_path = os.path.relpath(file_path, args.source)
        checksum_file_path = f'{file_path}.{args.extension}'

        if not os.path.exists(checksum_file_path):
            print(f'Checksum file does not exist for {file_path}. '
                  f'Creating it...')
            checksum_file_path = generate_checksum(file_path, 
                                                   args.extension,
                                                   args.algorithm)

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
                    print(f'Checksum does not match for '
                          f'{destination_file_path}.')

if __name__ == "__main__":
    main()
