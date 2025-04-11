"""
Write function which updates dictionary with defined values but only if new value more then in dict
Restriction: do not use .update() method of dictionary
Examples:
    >>> set_to_dict({'a': 1, 'b': 2, 'c': 3}, a=0, b=4)  # only b updated because new value for a less then original value
    {'a': 1, 'b': 4, 'c': 3}
    >>> set_to_dict({}, a=0)
    {a: 0}
    >>> set_to_dict({'a': 5})
    {'a': 5}
"""
from typing import Dict
import unittest


def set_to_dict(dict_to_update: Dict[str, int], **items_to_set) -> Dict[str, int]:
    for k, v in items_to_set.items():
        if dict_to_update.get(k) is not None and dict_to_update[k] >= v:
            continue
        dict_to_update[k] = v
    return dict_to_update


class TestSetToDict(unittest.TestCase):
    def test_update_dict_with_higher_values(self):
        self.assertEqual(set_to_dict({'a': 1, 'b': 2, 'c': 3}, a=0, b=4), {'a': 1, 'b': 4, 'c': 3})

    def test_empty_dict(self):
        self.assertEqual(set_to_dict({}, a=0), {'a': 0})

    def test_no_updates_needed(self):
        self.assertEqual(set_to_dict({'a': 5}), {'a': 5})

    def test_multiple_updates(self):
        self.assertEqual(set_to_dict({'a': 1, 'b': 2}, a=3, b=1), {'a': 3, 'b': 2})

if __name__ == '__main__':
    unittest.main()

