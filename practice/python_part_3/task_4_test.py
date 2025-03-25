"""
Create virtual environment and install Faker package only for this venv.
Write command line tool which will receive int as a first argument and one or more named arguments
 and generates defined number of dicts separated by new line.
Exec format:
`$python task_4.py NUMBER --FIELD=PROVIDER [--FIELD=PROVIDER...]`
where:
NUMBER - positive number of generated instances
FIELD - key used in generated dict
PROVIDER - name of Faker provider
Example:
`$python task_4.py 2 --fake-address=address --some_name=name`
{"some_name": "Chad Baird", "fake-address": "62323 Hobbs Green\nMaryshire, WY 48636"}
{"some_name": "Courtney Duncan", "fake-address": "8107 Nicole Orchard Suite 762\nJosephchester, WI 05981"}


My notes:
The way I solved this is I used the idea from a previous exercise
that we can use getattr() to allow for dynamic method calling,
so we don't need to hardcode the allowed providers.

Since argparse doesn't parse undefined keyword arguments,
I decided to use parse_known_args() which returns a list of unknown arguments
and parse them myself.
Another option would be to get a list of all providers (e.g. with dir())
and define them all in argparse.

"""



import argparse
import re
import faker
from unittest import mock


def parse_unknown_args(args_list):
    '''
    This function parses the unknown arguments returned by `parse_known_args()`
    only of the following form:
    ['--fake-address=address', '--some_name=name']
    and returns a dictionary like this:
    {'fake-address': 'address', 'some_name': 'name'}
    
    Note: argparse only parses arguments defined with `add_argument`, not arbitrary ones,
    so to parse arbitrary arguments you have to do it yourself:
    https://stackoverflow.com/a/9643809'''
    

    pattern = r"^--([^=]+)=([^=]+)$"

    args_dict = {}
    for arg_str in args_list:
        match = re.match(pattern, arg_str)
        if not match:
            raise ValueError(f"Argument has invalid format: {arg_str}")
        key, value = match.group(1, 2)
        args_dict[key] = value
    return args_dict


def test_parse_unknown_args():
    unknown = ['--fake-address=address', '--some_name=name']
    assert parse_unknown_args(unknown) == {'fake-address': 'address', 'some_name': 'name'}



def generate_record(key_provider_dict: dict[str, str], fake: faker.Faker) -> dict:
    result = {}
    for k, provider in key_provider_dict.items():
        try:
            func = getattr(fake, provider)
            # check that this is indeed a method that returns a string
            fake_value = func()
            assert isinstance(fake_value, str)
        except:
            raise ValueError(f"Invalid provider name {provider}")
        result[k] = fake_value
    return result


def generate_records(args_list: list[str] = None, fake = faker.Faker()) -> None:
    '''Takes the arguments as a list of strings,
    e.g. ['2', '--fake-address=address', '--some_name=name'].
    If unspecified, parse from stdin.
    '''
    parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')
    parser.add_argument('count', type=int)
    if args_list:
        namespace, unknown = parser.parse_known_args(args=args_list)
    else:
        namespace, unknown = parser.parse_known_args()
    
    count = namespace.count
    key_provider_dict = parse_unknown_args(unknown)  # mapping key name to Faker provider
    records = [generate_record(key_provider_dict, fake) for _ in range(count)]
    return records


if __name__ == "__main__":
    res = generate_records()
    print(res)



"""
Write test for print_name_address function
Use Mock for mocking args argument https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock
(you meant for mocking faker's provider methods?)
Example:
    >>> m = Mock()
    >>> m.method.return_value = 123
    >>> m.method()
    123
"""


def test_print_name_address():
    '''Mocking the result of the Faker instance, to know what fake values to expect'''
    fake = faker.Faker()
    mock_addr = 'mock-address'
    mock_name = 'mock-name'
    fake.address = mock.MagicMock(return_value=mock_addr)
    fake.name = mock.MagicMock(return_value=mock_name)
    records = generate_records(['2', '--fake-address=address', '--some_name=name'], fake)
    assert records == [{'fake-address': mock_addr, 'some_name': mock_name}, {'fake-address': mock_addr, 'some_name': mock_name}]
 