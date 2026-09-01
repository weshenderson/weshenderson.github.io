#!/usr/bin/env python3
"""
Display all metadata contained in a PDF document.

Defaults to resumes/resume.pdf but accepts a PDF path as the first
command-line argument.
"""
import sys

from pypdf import PdfReader

DEFAULT_PDF = "resumes/resume.pdf"

def get_pdf_file():
    """Return the PDF path from the command line or use the default."""

    return sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PDF

def display_metadata(pdf_file):
    """Display standard and XMP metadata from a PDF."""

    reader = PdfReader(pdf_file)

    print(f"PDF: {pdf_file}")
    print()

    print("Document Metadata")
    print("-----------------")

    if reader.metadata:
        for key, value in reader.metadata.items():
            print(f"{key}: {value}")
    else:
        print("No document metadata found.")

    print()

    print("XMP Metadata")
    print("------------")

    if reader.xmp_metadata:
        print(reader.xmp_metadata)
    else:
        print("No XMP metadata found.")


if __name__ == "__main__":
    display_metadata(get_pdf_file())
