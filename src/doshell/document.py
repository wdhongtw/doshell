import enum
import json
import os
import subprocess
import sys
import tempfile
from collections.abc import Callable
from typing import BinaryIO

import pypdf


class NameObject:
    """
    See: PDF 1.7 Reference 3.2.4 Name Objects
    """

    def __init__(self, name: str):
        self._name = name

    def value(self) -> str:
        return f"/{self._name}"


class Field(enum.StrEnum):
    """
    Fields for PDF metadata.

    See: PDF 1.7 Reference 10.2.1 Document Information Dictionary
    """

    Title = "Title"
    Subject = "Subject"
    Author = "Author"
    Creator = "Creator"
    Producer = "Producer"
    Keywords = "Keywords"
    CreationDate = "CreationDate"
    ModDate = "ModDate"
    Trapped = "Trapped"


def show_pdf_meta(file: BinaryIO) -> None:

    def show_meta(meta: pypdf.DocumentInformation | None):
        print(f"File: {file.name}")
        if meta is None:
            return

        def show_tag(tag: str) -> None:
            value = meta.get(NameObject(tag).value())
            print(f"    {tag}: {repr(value)}")

        for field in Field:
            show_tag(field)

    pdf = pypdf.PdfReader(file)
    show_meta(pdf.metadata)


def main_show_pdf_meta() -> None:
    if len(sys.argv) < 2:
        input("Usage: <command> <pdf-file>")
        return
    with open(sys.argv[1], "rb") as file:
        show_pdf_meta(file)


def edit_pdf_meta(source: BinaryIO, editor: str) -> Callable[[BinaryIO], None] | None:
    pdf = pypdf.PdfReader(source)
    record = {
        "title": pdf.metadata.title if pdf.metadata else None,
        "author": pdf.metadata.author if pdf.metadata else None,
    }
    with tempfile.TemporaryFile(mode="w+t") as file:
        json.dump(record, file)
        file.flush()
        subprocess.run(f"{editor} {file.name}", shell=True, check=True)
        file.seek(0)
        result = json.load(file)
    if result == record:
        return

    output = pypdf.PdfWriter(pdf)

    def write(destination: BinaryIO) -> None:
        output.add_metadata(
            {
                NameObject(Field.Title).value(): result["title"],
                NameObject(Field.Author).value(): result["author"],
            }
        )
        output.write(destination)

    return write


def main_edit_pdf_meta() -> None:
    if "EDITOR" not in os.environ:
        input("Require EDITOR environment variable")
        return
    if len(sys.argv) < 2:
        input("Usage: <command> <pdf-file>")
        return
    file = sys.argv[1]
    with open(file, "rb") as source:
        write_func = edit_pdf_meta(source, os.environ["EDITOR"])

    if write_func is None:
        print("Not modified")
        return
    with open(file, "wb") as destination:
        write_func(destination)
