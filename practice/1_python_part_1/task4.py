"""
Write function which receives list of integers. Calculate power of each integer and
subtract difference between original previous value and it's power. For first value subtract nothing.
Restriction:
Examples:
    >>> calculate_power_with_difference([1, 2, 3])
    [1, 4, 7]  # because [1^2, 2^2 - (1^2 - 1), 3^2 - (2^2 - 2)]
"""
from typing import List
import unittest


def calculate_power_with_difference(ints: List[int]) -> List[int]:
    prev = 0
    ls = []
    for i in ints:
        ls.append(i**2 - (prev**2 - prev))
        prev = i
    return ls


def functional_version(ints: List[int]) -> List[int]:
    return [(i**2 - (prev**2 - prev)) for prev, i in zip([0] + ints, ints)]


class TestCalculatePowerWithDifference(unittest.TestCase):
    
    def test(self):
        self.assertEqual(calculate_power_with_difference([1, 2, 3]), [1, 4, 7])
        self.assertEqual(calculate_power_with_difference([1, 2, 3, 4]), [1, 4, 7, 10])


    def test_functional(self):
        self.assertEqual(functional_version([1, 2, 3]), [1, 4, 7])
        self.assertEqual(functional_version([1, 2, 3, 4]), [1, 4, 7, 10])

if __name__ == '__main__':
    unittest.main()


