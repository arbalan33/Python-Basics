"""
Use function 'generate_words' to generate random words.
Write them to a new file encoded in UTF-8. Separator - '\n'.
Write second file encoded in CP1252, reverse words order. Separator - ','.

Example:
    Input: ['abc', 'def', 'xyz']

    Output:
        file1.txt (content: "abc\ndef\nxyz", encoding: UTF-8)
        file2.txt (content: "xyz,def,abc", encoding: CP1252)
"""


def generate_words(n: int = 20) -> list[str]:
    import string
    import random

    words = list()
    for _ in range(n):
        word = ''.join(random.choices(
            string.ascii_lowercase, k=random.randint(3, 10)))
        words.append(word)

    return words


def write_utf8(words: list[str], file_path: str) -> None:
    """Write words to a file in UTF-8 encoding with newline separation."""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(words))


def write_cp1252(words: list[str], file_path: str) -> None:
    """Write words to a file in CP1252 encoding with comma separation, reversed order."""
    with open(file_path, 'w', encoding='cp1252') as f:
        f.write(','.join(reversed(words)))
