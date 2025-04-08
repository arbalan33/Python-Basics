import argparse
import configparser
import json
import logging
import multiprocessing
import os
import sys
import pathlib
import traceback
import uuid

from interpreter import generate_object, ParsingError


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s\t%(levelname)s\t%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler()]
)


config = configparser.ConfigParser()
config.read('default.ini')
config_dict: dict = dict(config['DEFAULT'])

argparser = argparse.ArgumentParser(prog='myfaker',
                                    description='Utility for generating test data based on the provided data schema',
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
argparser.add_argument(
    'directory',
    default=config_dict.get('directory', 'out'),
    help='Path to directory in which to save generated files'
)

argparser.add_argument(
    '--data-schema', '-s',
    required=True,
    type=str,
    help='Schema string or path to JSON file with the schema'
)

argparser.add_argument(
    '--files-count', '-n',
    type=int,
    default=config_dict.get('files_count', 0),
    help='Number of files to generate'
)

argparser.add_argument(
    '--file-name', '-b',
    default=config_dict.get('file_name', 'myfaker_data'),
    help='Base filename of the created files'
)

argparser.add_argument(
    '--file-suffix', '-x',
    default=config_dict.get('file_suffix', 'uuid'),
    choices=['count', 'random', 'uuid'],
    help=(
        'Type of suffix to be appended to the base filename '
        'when more than one file is generated'
    )
)

argparser.add_argument(
    '--data-lines', '-l',
    type=int,
    default=config_dict.get('data_lines', 1),
    help='How many lines to generate in each file'
)

argparser.add_argument(
    '--clear-path', '-r',
    action='store_true',
    help='Delete existing files with the same base filename'
)

argparser.add_argument(
    '--multiprocessing', '-j',
    type=int,
    default=config_dict.get('multiprocessing', 1),
    help='Number of concurrent jobs (limited by CPU cores)'
)


def generate_files(directory: pathlib.Path, schema: str,
                   file_base_name: str, file_suffix: str,
                   files_count: int, data_lines: int) -> None:
    for i in range(files_count):
        if file_suffix == 'uuid':
            suffix = '_' + str(uuid.uuid4())
        elif file_suffix == 'int':
            suffix = '_' + str(i)
        elif file_suffix == 'random':
            suffix = '_' + str(uuid.uuid4())

        fpath = directory / (file_base_name + suffix + '.jsonl')

        for _ in range(data_lines):
            obj = generate_object(schema)
            with fpath.open('a') as f:
                f.write(json.dumps(obj) + '\n')


def generate_to_stdout(schema: str, count: int):
    for _ in range(count):
        obj = generate_object(schema)
        print(json.dumps(obj))


def clear_files_with_prefix(dir: pathlib.Path, prefix):
    '''Given a directory and a prefix string,
    delete all files with matching prefix in their filename from the directory'''

    for file in dir.iterdir():
        if file.is_file() and file.name.startswith(prefix):
            file.unlink()  # Delete the file


def run_cli(argv=None):
    '''Run the CLI app on the provided arguments,
    or on the sys.argv list if argv is None'''
    args = argparser.parse_args(argv)

    # Input validation

    try:
        out_dir = pathlib.Path(args.directory)
    except:
        raise ValueError('Can\'t find output directory')

    try:
        path = pathlib.Path(args.data_schema)
        schema = path.read_text()
    except:
        schema = args.data_schema

    if args.files_count < 0:
        raise ValueError('Files count cannot be negative')

    if args.multiprocessing < 1:
        raise ValueError('Multiprocessing must be a natural number')

    elif args.multiprocessing > os.cpu_count():
        args.multiprocessing = os.cpu_count()
        logging.info(
            f'Limited number of cores to {args.multiprocessing}')

    # Processing

    if args.clear_path and args.files_count != 0:
        clear_files_with_prefix(out_dir, args.file_name)

    logging.info('Generating data...')
    if args.files_count == 0:
        generate_to_stdout(schema, args.data_lines)
    else:
        generate_files(out_dir, schema, args.file_name, args.file_suffix,
                       args.files_count, args.data_lines)
    logging.info('Data generated')


if __name__ == '__main__':
    # redirect traceback to file
    try:
        run_cli()
    except ParsingError as e:
        logging.error("Syntax error: " + str(e))
        sys.exit(1)
    except ValueError as e:
        logging.error("Argument error: " + str(e))
        sys.exit(1)
    except Exception as e:
        logging.error("An unhandled exception occurred: " + str(e))
        with open('error_log.txt', 'a') as f:
            f.write(traceback.format_exc())
        sys.exit(1)
