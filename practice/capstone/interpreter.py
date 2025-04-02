import time
import uuid
import json
import re
import random
import logging
from typing import Union

'''
This module provides the `generate_object(spec)` function
which takes a spec string and returns a python object according to the spec.

---

The interpretation of a schema string happens in two steps:
1. Parsing the string into an AST
2. Evaluating the AST and returning the generated python object
   (which can then be converted to a JSON string)

The AST is represented with a python dict that looks like this:
{
    'date': ('timestamp', None),
    'name': ('str', ('rand',)),
    'type': ('str', ['client', 'partner', 'government']),
    'age': ('int', ('rand', 1, 90)),
    'str': ('str', 'cat1'),
    'num': ('int', 1),
}

I didn't write a specification for the AST on purpose,
because in a real scenario the AST would change very often.
However, i did write unit tests for the parser which act as a specification.

Syntax of the shema string:
  Schema is a valid JSON object where values are strings called "field specifiers".
  E.g. {"name": "str:", "age": "int:rand(1, 100)"}

  The field specifier has the following syntax:
  field_spec := \" field_type ":" field_modifier \"

  A field_modifier is one of:
  - "rand"
  - "rand(<int1>, <int2>)"
    (e.g. "rand(1, 2)")
  - list of strings/ints
    (e.g. ['a', 'b'])
  - string literal (starting with a letter, only alphanumerics)
  - integer
  - an empty string ("")

On any syntax error, the parser raises the custom ParsingError exception.
Some syntax errors are only detected during evaluation,
which is a trade-off made to simplify the parser.
(Not that it makes any difference in this simple program)
'''


class ParsingError(Exception):
    """Raised when the input string does not match the expected grammar."""
    pass


def parse_field_modifier(s: str) -> Union[int, str, float]:
    '''The field modifier is parsed separately from the field type for simplicity,
    but this also means we can't detect some syntax errors during parsing.'''
    if s == '':
        return None

    if s[0] == '[':
        # convert single quotes to double quotes to parse as json
        s = s.replace("'", '"')

        try:
            ls = json.loads(s)
            assert isinstance(ls, list)
        except:
            raise ParsingError('Malformed list in field spec')

        if len(ls) == 0:
            raise ParsingError('List must have at least one element')

        return ls

    if s == 'rand':
        return ('rand',)

    match = re.search(r"rand\((\w+),\s*(\w+)\)", s)
    if match:
        try:
            int1, int2 = (int(n) for n in match.groups())
        except:
            raise ParsingError('Arguments to rand must be two integers')
        return ('rand', int1, int2)

    # as a last resort, it must be either a string or an int value

    if s[0].isdigit():
        try:
            n = int(s)
            return n
        except ValueError:
            raise ParsingError('Malformed integer value')

    if not s.isalnum():
        raise ParsingError('String value must be alphanumeric')

    return s


def parse_field_spec(s: str) :
    '''For example "int:range(1, 10)"
    '''
    field_type, field_modifier_s = s.split(':')

    if field_type not in ('int', 'str', 'timestamp'):
        raise ParsingError('Invalid field type')

    field_modifier = parse_field_modifier(field_modifier_s)

    return (field_type, field_modifier)


def parse(s: str) -> dict[str, tuple]:
    '''Takes a spec string and returns an AST'''
    try:
        obj = json.loads(s)
        assert isinstance(obj, dict)
    except:
        raise ParsingError('Wrong syntax of the key-value mapping')

    if len(obj) == 0:
        raise ParsingError("At least one field spec is required")

    AST = {name: parse_field_spec(v) for name, v in obj.items()}
    return AST


def evaluate_field_spec(spec: tuple[str, any]):
    typ, modi = spec

    # timestamp is the same no matter the modifier
    if typ == 'timestamp':
        if modi != None:
            logging.warning('Modifiers are ignored in timestamp field')
        return time.time()

    # empty spec after type
    if modi is None:
        return '' if typ == 'str' else None

    # literal values are returned as-is (int and str)
    if isinstance(modi, int):
        if typ != 'int':
            raise ParsingError("Wrong field type for int value")
        return modi
    if isinstance(modi, str):
        if typ != 'str':
            raise ParsingError("Wrong field type for str value")
        return modi

    # random
    if isinstance(modi, tuple) and modi[0] == 'rand':
        if typ == 'str':
            if len(modi) != 1:
                raise ParsingError(
                    'String fields don\'t support rand with range')
            return str(uuid.uuid4())

        # random ints
        if typ == 'int' and modi == ('rand',):
            return random.randint(0, 10000)
        # wish i could use the match block here
        if typ == 'int' and modi[0] == 'rand' and len(modi) == 3:
            _, start, end = modi
            return random.randint(start, end)

    # lists
    if isinstance(modi, list):
        if typ == 'str':
            if not all(isinstance(item, str) for item in modi):
                raise ParsingError(
                    'List items of a string field must be strings')

        if typ == 'int':
            if not all(isinstance(item, int) for item in modi):
                raise ParsingError('List items of a string field must be ints')

        return random.choice(modi)

    return None


def evaluate(ast: dict) -> dict[str, any]:
    return {name: evaluate_field_spec(spec) for name, spec in ast.items()}


def generate_object(spec_str: str) -> dict[str, any]:
    return evaluate(parse(spec_str))


if __name__ == "__main__":
    
    # Example usage
    spec_str = '''
        {
        "date":"timestamp:rand",
        "name": "str:rand",
        "type":"str:['client', 'partner', 'government']",
        "age": "int:rand(1, 90)",
        "str": "str:cat1",
        "num": "int:1"
        }
        '''
    print(generate_object(spec_str))
