"""
Generate and apply Alea build provenance metadata 
collected from the GitHub Actions environment:

{
    "meta": {
        "buildData": {
            "build": "...",
            "runId": "...",
            "attempt": "...",
            "commit": "...",
            "date": "..."
        }
    }
}

No build metadata is generated outside of CI.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from docx import Document

class DocxMetadata:
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

        return {"meta": {"buildData": build_data}}

    def update_docx_metadata(build_data, docx_file='resumes/resume.docx'):
        """Add build provenance to a DOCX document's comments property."""

        document = Document(docx_file)

        json_payload = json.dumps(
            build_data,
            separators=(",", ":")
        )

        document.core_properties.comments = json_payload

        document.save(docx_file)

        print(f"Updated DOCX metadata: {docx_file}")

    def apply_build_metadata():
        """Generate build metadata and update the DOCX artifact."""

        build_data = DocxMetadata.get_build_data()

        if build_data is None:
            return

        print("Alea build metadata:")
        print(json.dumps(build_data, indent=2))

        docx_file = Path("resumes/resume.docx")

        if docx_file.is_file():
            DocxMetadata.update_docx_metadata(build_data, docx_file)
        else:
            print(f"DOCX file not found: {docx_file}")
