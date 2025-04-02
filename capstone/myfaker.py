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
defaults: dict = dict(config['DEFAULT'])

argparser = argparse.ArgumentParser(prog='myfaker',
                                    description='Utility for generating test data based on the provided data schema',
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
argparser.add_argument(
    'directory',
    default=defaults.get('file_suffix', 'uuid'),
    help='Path to directory in which to save generated files'
)

argparser.add_argument(
    '--files-count',
    type=int,
    default=defaults.get('files_count', 0),
    help='Number of files to generate'
)

argparser.add_argument(
    '--file-name',
    default=defaults.get('file_name', 'myfaker_data'),
    help='Base filename of the created files'
)

argparser.add_argument(
    '--file-suffix',
    default=defaults.get('file_suffix', 'uuid'),
    choices=['count', 'random', 'uuid'],
    help=(
        'Type of suffix to be appended to the base filename '
        'when more than one file is generated'
    )
)

argparser.add_argument(
    '--data-lines',
    type=int,
    default=defaults.get('data_lines', 10),
    help='How many lines to generate in each file'
)

argparser.add_argument(
    '--clear-path',
    action='store_true',
    help='Delete existing files with the same base filename'
)

argparser.add_argument(
    '--multiprocessing',
    type=int,
    default=defaults.get('multiprocessing', 1),
    help='Number of concurrent jobs (limited by CPU cores)'
)

argparser.add_argument(
    '--data-schema',
    required=True,
    type=str,
    help='Schema string or path to JSON file with the schema'
)


def generate_files(schema: str, file_base_name: str, file_suffix: str,
                   files_count: int, data_lines: int) -> None:
    for i in range(files_count):
        if file_suffix == 'uuid':
            suffix = '_' + str(uuid.uuid4())
        elif file_suffix == 'int':
            suffix = '_' + str(i)
        elif file_suffix == 'random':
            # TODO random??
            suffix = '_' + str(i)
        fpath = pathlib.Path(file_base_name + suffix + '.jsonl')
        
        for _ in range(data_lines):
            obj = generate_object(schema)
            with fpath.open('a') as f:
                f.write(json.dumps(obj) + '\n')


def generate_to_stdout(schema: str, count: int):
    for _ in range(count):
        obj = generate_object(schema)
        print(json.dumps(obj))


def run_cli():
    args = argparser.parse_args()

    # Input validation

    try:
        path = pathlib.Path(args.data_schema)
        schema = path.read_text()
    except:
        schema = args.data_schema

    # clear_path is an activation flag, so we have to set its default like this
    args.clear_path = defaults.get('clear_path', args.clear_path)

    if args.files_count < 0:
        logging.error('Files count cannot be negative')
        exit(1)

    if args.multiprocessing < 1:
        logging.error('Multiprocessing must be a natural number')
        exit(1)

    elif args.multiprocessing > os.cpu_count():
        args.multiprocessing = os.cpu_count()
        logging.info(
            f'Limited number of cores to {args.multiprocessing}')

    # Processing

    logging.info('Generating data...')
    if args.files_count == 0:
        generate_to_stdout(schema, args.data_lines)
    else:
        generate_files(schema, args.file_name, args.file_suffix,
                       args.files_count, args.data_lines)
    logging.info('Data generated')


if __name__ == '__main__':
    try:
        run_cli()
    except ParsingError as e:
        logging.error("Syntax error: " + str(e))
        sys.exit(1)  # Ensure a non-zero exit code for errors
    except Exception as e:
        logging.error("An unhandled exception occurred: " + str(e))
        with open('error_log.txt', 'a') as f:
            f.write(traceback.format_exc())
        sys.exit(1)  # Ensure a non-zero exit code for errors
