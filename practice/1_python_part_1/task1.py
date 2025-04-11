"""
Write function which deletes defined element from list.
Restriction: Use .pop method of list to remove item.
Examples:
    >>> delete_from_list([1, 2, 3, 4, 3], 3)
    [1, 2, 4]
    >>> delete_from_list(['a', 'b', 'c', 'b', 'd'], 'b')
    ['a', 'c', 'd']
    >>> delete_from_list([1, 2, 3], 'b')
    [1, 2, 3]
    >>> delete_from_list([], 'b')
    []
"""
from typing import TypeVar
import unittest


T = TypeVar('T')
def delete_from_list(list_to_clean: list[T], item_to_delete: any) -> list[T]:
    for i in reversed(range(len(list_to_clean))):
        if list_to_clean[i] == item_to_delete:
            list_to_clean.pop(i)
    return list_to_clean


class TestDeleteFromList(unittest.TestCase):
    def test_remove_existing_element(self):
        self.assertEqual(delete_from_list([1, 2, 3, 4, 3], 3), [1, 2, 4])
        self.assertEqual(delete_from_list(['a', 'b', 'c', 'b', 'd'], 'b'), ['a', 'c', 'd'])

    def test_remove_non_existent_element(self):
        self.assertEqual(delete_from_list([1, 2, 3], 'b'), [1, 2, 3])

    def test_empty_list(self):
        self.assertEqual(delete_from_list([], 'b'), [])


if __name__ == "__main__":
    unittest.main()