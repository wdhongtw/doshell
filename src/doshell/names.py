import string
import sys
import os
import pathlib
from collections.abc import Callable


def fmap[T](items: list[T], split: Callable[[T], list[T]]) -> list[T]:
    return [t for item in items for t in split(item)]


def to_kebab(name: str) -> str:
    chunks = [name]
    chunks = fmap(chunks, lambda w: w.split(" "))
    chunks = fmap(chunks, lambda w: w.split("_"))
    chunks = fmap(chunks, lambda w: w.split("-"))

    alphabet = set(string.ascii_letters + string.digits)

    apostrophe = set("'" + "\U00002019")
    with_apostrophe = lambda c: len(c) > 2 and c[-2] in apostrophe

    def normalize(chunk: str) -> str:
        chunk = chunk.lower()
        chunk = chunk[None:-2] if with_apostrophe(chunk) else chunk
        return "".join(c for c in chunk if c in alphabet)

    results = [normalize(c) for c in chunks]
    return "-".join(c for c in results if c)


def main_kebab() -> None:
    if len(sys.argv) != 2:
        input("Usage: <command> <file>")
        return

    file = sys.argv[1]
    ext = "".join(pathlib.Path(file).suffixes)  # support files like log.tar.gz
    stem = sys.argv[1].replace(ext, "")
    normalized = to_kebab(stem) + ext
    if normalized == sys.argv[1]:
        return
    os.rename(file, normalized)
