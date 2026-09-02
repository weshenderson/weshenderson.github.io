"""
Generate and apply Alea build provenance metadata
collected from the GitHub Actions environment:

No build metadata is generated outside of CI.
"""

import json
from pathlib import Path

from docx import Document
from pypdf import PdfReader, PdfWriter

from .alea_helper_functions import AleaHelperFunctions

class RenderMetadata:
    """Apply build metadata and apply to the artifact(s)."""

    @staticmethod
    def apply_docx_metadata(build_data, docx):
        """Add build provenance to a DOCX document's comments property."""

        document = Document(docx)

        json_payload = json.dumps(
            build_data,
            separators=(",", ":")
        )

        document.core_properties.comments = json_payload

        document.save(docx)

        print(f"Updated DOCX metadata: {docx}")

    @staticmethod
    def apply_pdf_metadata(build_data, pdf):
        """Add Alea build provenance to the PDF metadata."""

        reader = PdfReader(pdf)
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

        writer.write(pdf)

        print(f"Updated PDF metadata: {pdf}")

    def render(self, dest):
        """Apply build metadata to the provided artifact (DOCX & PDF supported)."""

        dest = Path(dest)

        helper     = AleaHelperFunctions()
        build_data = helper.get_build_metadata()

        if build_data is None:
            return

        print("Alea build metadata:")
        print(json.dumps(build_data, indent=2))

        if not dest.is_file():
            print(f"File not found: {dest}")
            return

        file_type = Path(dest).suffix

        if file_type == ".docx":
            self.apply_docx_metadata(build_data, dest)
        elif file_type == ".pdf":
            self.apply_pdf_metadata(build_data, dest)
        else:
            print(f"Unsupported file type: {file_type}")
