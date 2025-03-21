"""
Write function which receives line of space sepparated words.
Remove all duplicated words from line.
Restriction:
Examples:
    >>> remove_duplicated_words('cat cat dog 1 dog 2')
    'cat dog 1 2'
    >>> remove_duplicated_words('cat cat cat')
    'cat'
    >>> remove_duplicated_words('1 2 3')
    '1 2 3'
"""

from collections import Counter


def remove_duplicated_words(line: str) -> str:
    unique_words: list[str] = list(Counter(line.split()).keys())
    return ' '.join(unique_words)


import unittest

class TestRemoveDuplicatedWords(unittest.TestCase):
    
    def test_basic_case(self):
        self.assertEqual(remove_duplicated_words('cat cat dog 1 dog 2'), 'cat dog 1 2')
    
    def test_all_duplicates(self):
        self.assertEqual(remove_duplicated_words('cat cat cat'), 'cat')
    
    def test_no_duplicates(self):
        self.assertEqual(remove_duplicated_words('1 2 3'), '1 2 3')
    
if __name__ == '__main__':
    unittest.main()

