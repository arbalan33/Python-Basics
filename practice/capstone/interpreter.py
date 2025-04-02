import time
import uuid
import json
import re
import random
import logging

'''
Syntax:
  Schema looks like a JSON object where values are strings called "field specifiers":
  schema := '{' (<name> ':' <field_spec>)*  '}'
  E.g. {"name": "str:"}

  field_spec := \" <field_type> ":" <field_modifier> \"

'''


class ParsingError(Exception):
    """Raised when the input string does not match the expected grammar."""
    pass


def parse_field_modifier(s: str):
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


def parse_field_spec(s):
    field_type, field_modifier_s = s.split(':')

    if field_type not in ('int', 'str', 'timestamp'):
        raise ParsingError('Invalid field type')

    field_modifier = parse_field_modifier(field_modifier_s)

    return (field_type, field_modifier)


def parse(s: str):
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

    # timestamp is returned no matter the modifier
    if typ == 'timestamp':
        if modi != None:
            logging.warning('Modifiers are ignored in timestamp field')
        return time.time()

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


def evaluate(ast: dict):
    return {name: evaluate_field_spec(spec) for name, spec in ast.items()}
