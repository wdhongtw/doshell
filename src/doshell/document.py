from typing import BinaryIO
import sys
import enum
from typing import Any

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
        print(f"===== {file.name} =====")
        if meta is None:
            print("No meta data")
            return None

        def show_tag(tag: str) -> None:
            value = meta.get(NameObject(tag).value())
            print(f"{tag}: {repr(value)}")

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
