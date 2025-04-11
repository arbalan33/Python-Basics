"""
Read files from ./files and extract values from them.
Write one file with all values separated by commas.

Example:
    Input:

    file_1.txt (content: "23")
    file_2.txt (content: "78")
    file_3.txt (content: "3")

    Output:

    result.txt(content: "23, 78, 3")
"""

from pathlib import Path


def read_files_from_dir(directory: str) -> list[str]:
    contents = []
    for file_path in Path(directory).iterdir():
        if file_path.is_file():
            try:
                with file_path.open("r") as f:
                    contents.append(f.read().strip())
            except (ValueError, FileNotFoundError):
                continue
    return contents


def safe_int(s: str) -> bool:
    try:
        int(s)
        return True
    except ValueError:
        return False
    

def extract_numbers_from_files(directory: str, output_file: str = "result.txt") -> None:
    contents = read_files_from_dir(directory)    
    numbers = [int(s) for s in contents if safe_int(s)]
    output = ', '.join(str(n) for n in numbers)

    with open(output_file, "w") as f:
        f.write(output)


if __name__ == "__main__":
    extract_numbers_from_files("practice/python_part_2/files")
