from interpreter import parse, ParsingError, evaluate

import pytest


@pytest.mark.parametrize(
    ('inp', 'expected_AST'),
    [

        # 'rand' is a keyword, not a string
        (
            '{"name": "timestamp:rand"}',
            {'name': ('timestamp', ('rand',))}
        ),

        # 'rand(1, 2)'
        (
            '{"name": "timestamp:rand(1, 2)"}',
            {'name': ('timestamp', ('rand', 1, 2))}
        ),

        # empty value spec is always None (for any type)
        (
            '{"name": "str:"}',
            {'name': ('str', None)}
        ),


        # list with one item
        (
            '''{"name": "str:['item']"}''',
            {'name': ('str', ['item'])}
        ),

        # list with two items
        (
            '''{"name": "str:['item', 'second']"}''',
            {'name': ('str', ['item', 'second'])}
        ),

        # list of ints
        (
            '''{"name": "str:[1, 2]"}''',
            {'name': ('str', [1, 2])}
        ),

        # string value other than rand
        (
            '{"name": "str:name1"}',
            {'name': ('str', 'name1')}
        ),


        # value spec starts with 'rand' but is just a string
        (
            '{"name": "str:random"}',
            {'name': ('str', 'random')}
        ),

        # int value
        (
            '{"name": "str:1"}',
            {'name': ('str', 1)}
        ),


        (
            '''
         {"date":"timestamp:",
        "name": "str:rand",
        "type":"str:['client', 'partner', 'government']",
        "age": "int:rand(1, 90)",
        "str": "str:cat1",
        "num": "int:1"}
         ''',
            {'date': ('timestamp', None),
             'name': ('str', ('rand',)),
             'type': ('str', ['client', 'partner', 'government']),
             'age': ('int', ('rand', 1, 90)),
             'str': ('str', 'cat1'),
             'num': ('int', 1),
             }
        )
    ])
def test_parse(inp, expected_AST):
    assert parse(inp) == expected_AST


@pytest.mark.parametrize(
    "inp",
    [
        # invalid JSON
        'test.txt',

        # at least one field spec required
        '{}',

        # rand arguments must be int
        '{"name": "int:rand(a, b)"}',

        # at least one element required in list
        '''{"name": "str:[]"}''',

        # string value can only contain alphanumeric chars
        '{"name": "str:a1+"}',

        # integer value
        '{"name": "str:1e"}',
    ])
def test_raises(inp):
    with pytest.raises(ParsingError):
        parse(inp)


def test_fields_count():
    ast = {'num': ('int', ('rand',)),
           'f': ('str', 'test')}
    res = evaluate(ast)
    assert isinstance(res, dict)
    assert list(res.keys()) == ['num', 'f']


def test_rand_int():
    ast = {'num': ('int', ('rand',))}
    res = evaluate(ast)
    assert isinstance(res['num'], int)

    ast = {'num': ('int', ('rand', 1, 1))}
    res = evaluate(ast)
    assert res['num'] == 1


def test_rand_str():
    ast = {'f': ('str', ('rand',))}
    res = evaluate(ast)
    assert isinstance(res['f'], str)


def test_literal_values():
    ast = {'f': ('str', 'a1')}
    res = evaluate(ast)
    assert res['f'] == 'a1'


def test_list():
    ast = {'f': ('str', ['1', '2'])}
    res = evaluate(ast)
    assert res['f'] in ['1', '2']

    ast = {'f': ('int', [1, 2])}
    res = evaluate(ast)
    assert res['f'] in [1, 2]


def test_empty_string():
    ast = {'f': ('str', None)}
    res = evaluate(ast)
    assert res['f'] == ''


def test_empty_int():
    ast = {'f': ('int', None)}
    res = evaluate(ast)
    assert res['f'] is None


def test_timestamp():
    ast = {'f': ('timestamp', 'test')}
    res = evaluate(ast)
    assert isinstance(res['f'], float)


@pytest.mark.parametrize(
    "ast",
    [
        # all items of a list must have the appropriate type
        {'f': ('int', ['test', 1])},
        {'f': ('str', ['test', 1])},

        # can't do rand range for string type
        {'f': ('str', ('rand', 1, 2))},
    ])
def test_evaluate_raises(ast):
    with pytest.raises(ParsingError):
        evaluate(ast)
