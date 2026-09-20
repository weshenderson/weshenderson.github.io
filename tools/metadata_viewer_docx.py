#!/usr/bin/env python3
# pylint: skip-file
"""
Display all metadata contained in a DOCX document.

Defaults to resumes/resume.docx but accepts a DOCX path as the first
command-line argument.
"""

import sys

from docx import Document

DEFAULT_DOCX = "public/resumes/resume.docx"


def get_docx_file():
    """Return the DOCX path from the command line or use the default."""

    return sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DOCX


def display_metadata(docx_file):
    """Display standard DOCX document metadata."""

    document = Document(docx_file)
    properties = document.core_properties

    print(f"DOCX: {docx_file}")
    print()

    print("Document Metadata")
    print("-----------------")

    metadata = {
        "Title": properties.title,
        "Subject": properties.subject,
        "Author": properties.author,
        "Keywords": properties.keywords,
        "Comments": properties.comments,
        "Category": properties.category,
        "Created": properties.created,
        "Modified": properties.modified,
        "Last Modified By": properties.last_modified_by,
        "Revision": properties.revision,
    }

    if any(value is not None for value in metadata.values()):
        for key, value in metadata.items():
            if value:
                print(f"{key}: {value}")
    else:
        print("No document metadata found.")


if __name__ == "__main__":
    display_metadata(get_docx_file())
