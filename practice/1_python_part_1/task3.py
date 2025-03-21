"""
Write function which receives list of text lines (which is space separated words) and word number.
It should enumerate unique words from each line and then build string from all words of given number.
Restriction: word_number >= 0
Examples:
    >>> build_from_unique_words('a b c', '1 1 1 2 3', 'cat dog milk', word_number=1)
    'b 2 dog'
    >>> build_from_unique_words('a b c', '', 'cat dog milk', word_number=0)
    'a cat'
    >>> build_from_unique_words('1 2', '1 2 3', word_number=10)
    ''
    >>> build_from_unique_words(word_number=10)
    ''
"""
import unittest
from collections import Counter

def build_from_unique_words(*lines: tuple[str], word_number: int) -> str:
    words = []
    for l in lines:
        # Counter (dict) remembers insertion order
        c = Counter(l.split())
        try:
            word = list(c.keys())[word_number]
        except IndexError:
            continue
        words.append(word)

    return ' '.join(words)


class TestBuildFromUniqueWords(unittest.TestCase):
    def test_valid_cases(self):
        self.assertEqual(build_from_unique_words('a b c', '1 1 1 2 3', 'cat dog milk', word_number=1), 'b 2 dog')
        self.assertEqual(build_from_unique_words('a b c', '', 'cat dog milk', word_number=0), 'a cat')
    
    def test_no_matching_word_number(self):
        self.assertEqual(build_from_unique_words('1 2', '1 2 3', word_number=10), '')
    
    def test_empty_input(self):
        self.assertEqual(build_from_unique_words(word_number=10), '')

if __name__ == '__main__':
    unittest.main()
