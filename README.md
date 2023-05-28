# check_copied_files - Checksum Validator

This Python command-line tool generates checksums for files in a source directory and optionally checks them against files in a destination directory. If a destination directory is not provided, the tool simply generates checksums in the source directory.

## Features

- Generate checksums for all files in a source directory
- Optionally check files against their checksums in a destination directory
- Exclude checksum files from processing
- Specify a file name filter to choose which files to process
- Choose the checksum algorithm to use (MD5 by default)

## Usage

To use the tool, run the following command in your terminal:

```
python check_copied_files.py -s SOURCE [-d DESTINATION] [-f FILTER] [-e EXTENSION] [-a ALGORITHM] [-c]
```

or

```
./check_copied_files.py -s SOURCE [-d DESTINATION] [-f FILTER] [-e EXTENSION] [-a ALGORITHM] [-c]
```

Replace `SOURCE` with the path to the source directory, and replace any optional arguments in square brackets as needed. Here are the details for each argument:

- `-s SOURCE` or `--source SOURCE`: (Required) Path to the source directory.
- `-d DESTINATION` or `--destination DESTINATION`: (Optional) Path to the destination directory. If not provided, the tool only generates checksums without checking any files.
- `-f FILTER` or `--filter FILTER`: (Optional) File name filter. By default, all files are processed. Checksum files are always excluded.
- `-e EXTENSION` or `--extension EXTENSION`: (Optional) Extension for the checksum files. By default, the extension is "checksum".
- `-a ALGORITHM` or `--algorithm ALGORITHM`: (Optional) Checksum algorithm. By default, the MD5 algorithm is used. You can specify any algorithm guaranteed to be supported by Python's `hashlib` module. The list of such algorithms can be found in the [hashlib module documentation](https://docs.python.org/3/library/hashlib.html).
- `-c` or `--force-check`: (Optional) Force checking files against checksum in the source folder if a checksum file exists for that file.

To see the list of all arguments and their descriptions, run the command with the `-h` or `--help` option:

```
python check_copied_files.py --help
```

## Requirements

This tool requires several Python packages. 

Here is the command to install the required packages using pip:

```
pip install glob2 tqdm
```

Or if you are using `conda`, run:

```
conda install -c anaconda glob2 tqdm
```

## Dependencies

The dependencies for this project are listed in the `requirements.txt` file for pip and in the `environment.yml` file for conda.

To install dependencies using pip:

```
pip install -r requirements.txt
```

To create a new conda environment with the necessary dependencies:

```
conda env create -f environment.yml
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)