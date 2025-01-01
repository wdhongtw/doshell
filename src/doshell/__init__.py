import sys
import zipfile
import pathlib
import os

from typing import IO
from collections.abc import Callable


def extract_japan(name: str, dir: str) -> None:
    """
    Extract with default locale to page 932 (Japan Shift-JIS) if not unicode.
    """
    file = zipfile.ZipFile(name, "r", metadata_encoding="932")
    file.extractall(dir)


def main_extract_japan() -> None:
    if len(sys.argv) != 2:
        input("Usage: <command> <zip-file>")
        return
    name = sys.argv[1]
    stem = pathlib.Path(name).stem
    print(f"Extracting: {name} to current directory")
    dir = pathlib.Path(os.getcwd()) / stem
    dir.mkdir(exist_ok=True)
    extract_japan(name, str(dir))


def zip_folder(
    folder_path: str, *, compress: bool = False
) -> Callable[[IO[bytes]], None]:
    """
    Pack the folder as a ZIP without compression.
    """

    mode = zipfile.ZIP_DEFLATED if compress else zipfile.ZIP_STORED

    def write(file: IO[bytes]) -> None:
        with zipfile.ZipFile(file, "w", mode) as archive:
            for root, _, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    archive.write(file_path, os.path.relpath(file_path, folder_path))

    return write


def main_pack_cbz() -> None:

    if len(sys.argv) != 2:
        input("Usage: <command> <folder>")
        return
    folder_path = sys.argv[1]
    zip_path = f"{folder_path}.cbz"

    with open(zip_path, "wb") as file:
        zip_folder(folder_path)(file)
