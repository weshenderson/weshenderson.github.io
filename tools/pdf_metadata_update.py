#!/usr/bin/env python3
# pylint: skip-file
"""
Generate and apply Alea build provenance metadata (PDF)
collected from the GitHub Actions environment:

No build metadata is generated outside of CI.

Note: PDF operations currently exist outside of Alea. This
      will eventually be moved into the main codebase.
"""

import json
import os
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

from pypdf import PdfReader, PdfWriter

DEFAULT_PDF = "resumes/resume.pdf"

def get_pdf_file():
    """Return the PDF path from the command line or use the default."""

    return sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PDF

def get_build_data():
    """Return GitHub Actions build metadata in the canonical format."""

    environment_variables = {
        "Build": "GITHUB_RUN_NUMBER",
        "Run ID": "GITHUB_RUN_ID",
        "Attempt": "GITHUB_RUN_ATTEMPT",
        "Commit": "GITHUB_SHA",
    }

    missing_variables = [
        variable
        for variable in environment_variables.values()
        if not os.getenv(variable)
    ]

    if missing_variables:
        print("Not running in the GitHub Actions build environment.")
        return None

    build_data = {
        key: os.environ[variable]
        for key, variable in environment_variables.items()
    }

    central_time = datetime.now(
        ZoneInfo("America/Chicago")
    )

    build_data["Date"] = central_time.strftime(
        "%Y-%m-%d %I:%M:%S %p %Z"
    )

    return {
        "meta": {
            "buildData": build_data
        }
    }

def update_pdf_metadata(pdf_file, build_data):
    """Add Alea build provenance to the PDF metadata."""

    reader = PdfReader(pdf_file)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    # Preserve existing PDF metadata.
    if reader.metadata:
        writer.add_metadata(reader.metadata)

    json_payload = json.dumps(
        build_data,
        separators=(",", ":")
    )

    # Store the provenance payload in PDF Keywords.
    writer.add_metadata({
        "/Keywords": json_payload
    })

    writer.write(pdf_file)

    print(f"Updated PDF metadata: {pdf_file}")

def apply_build_metadata():
    """Generate build metadata and apply it to the PDF artifact."""

    build_data = get_build_data()

    if build_data is None:
        return

    print("Alea build metadata:")
    print(json.dumps(build_data, indent=2))

    pdf_file = get_pdf_file()

    update_pdf_metadata(pdf_file, build_data)

if __name__ == "__main__":
    apply_build_metadata()
