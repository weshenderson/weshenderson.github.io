#!/usr/bin/env python3
"""
Author: Wes Henderson

Generate website and resume artifacts from the project's YAML configuration.

Alea is the command-line entry point for generating, validating, and backing
up website and resume assets. Individual resume formats can be generated
independently, or grouped operations can be used to generate complete sets
of artifacts.

TODO:
  * Add validation and creation options for CONFIG_FILE (.alea.yaml).
  * Add option to change the number of jobs displayed.
  * Add HTML, CSS, and Markdown validation.
  * Expand schema definitions:
    * education
    * certifications
    * skills
    * work
  * Add a 'Selected Projects' section to the resume?
  * Spec recommendations:
    - 'location' for school
        - Issue: https://github.com/jsonresume/resume-schema/issues/417
    - 'license' for certificate
    - meta details for site and googleAnalytics
    - add currentEmployee key for work history
        - Issue: https://github.com/jsonresume/resume-schema/issues/410
"""

import argparse
import sys

from src import config
from src import AleaHelperFunctions
from src import RenderDocx
from src import RenderJson
from src import RenderPdf
from src import RenderTemplates
from src import RenderMetadata
from src import ValidateSchema

# pylint: disable=too-many-locals,too-many-branches,too-many-statements
def main():
    """Entrypoint for Alea."""

    json      = RenderJson()
    templates = RenderTemplates()
    docx      = RenderDocx()
    pdf       = RenderPdf()
    metadata  = RenderMetadata()
    schema    = ValidateSchema()

    def render_json():
        """Generate and validate the JSON resume."""

        destination = config['templates']['resume']['json']['destination']

        json.render(config['configs'], destination)
        metadata.render(destination)
        schema.json_resume(destination)

    def render_templates():
        """Generate the templated resumes (HTML and Markdown)."""

        templates.render("resume", config)

    def render_docx():
        """Generate and validate the ATS DOCX resume."""

        destination = config['templates']['resume']['docx']['destination']

        docx.render(destination)
        docx.validate_resume(destination)
        metadata.render(destination)

    def render_pdf():
        """Generate the PDF resume."""

        pdf.render(config['configs']['docker']['pdf']['project_directory'])
        metadata.render(config['templates']['resume']['pdf']['destination'])

    def render_website():
        """Generate all website artifacts."""

        schema.website(config['configs']['website'])
        templates.render("website", config)

    actions = {
        "json": render_json,
        "templates": render_templates,
        "docx": render_docx,
        "pdf": render_pdf,
    }

    resume_actions = (
        "json",
        "templates",
        "docx",
        "pdf",
    )

    description = (
        "Generate/validate website and resume artifacts."
    )

    epilog = (
        "Examples:\n"
        "  alea --resume       Generate all resume artifacts.\n"
        "  alea --website      Generate all website artifacts.\n"
        "  alea --json         Generate the JSON resume.\n"
        "  alea --docx         Generate the ATS resume.\n"
        "  alea --all          Generate all website and resume artifacts.\n"
        "  alea --validate -r  Validate the resume configuration.\n"
        "  alea --backup -r    Backup resume templates before editing.\n"
    )

    job_options = argparse.ArgumentParser(
        description=description,
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    job_options.add_argument(
        "-r",
        "--resume",
        action="store_true",
        help="Generate all resume artifacts.",
    )
    job_options.add_argument(
        "-w",
        "--website",
        action="store_true",
        help="Generate all website artifacts.",
    )
    job_options.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="Generate all website and resume artifacts.",
    )
    job_options.add_argument(
        "-j",
        "--json",
        action="store_true",
        help="Generate and validate the JSON resume.",
    )
    job_options.add_argument(
        "-t",
        "--templates",
        action="store_true",
        help="Generate the templated resumes (HTML and Markdown).",
    )
    job_options.add_argument(
        "-d",
        "--docx",
        action="store_true",
        help="Generate and validate the ATS DOCX resume.",
    )
    job_options.add_argument(
        "-p",
        "--pdf",
        action="store_true",
        help="Generate the PDF resume.",
    )
    job_options.add_argument(
        "-b",
        "--backup",
        action="store_true",
        help="Back up website and/or resume templates.",
    )
    job_options.add_argument(
        "-v",
        "--validate",
        action="store_true",
        help="Validate the requested website and/or resume configuration.",
    )

    args = job_options.parse_args()

    website_requested = args.website or args.all
    resume_requested = (
        args.resume
        or args.all
        or any(
            getattr(args, artifact)
            for artifact in resume_actions
        )
    )

    if args.validate:
        if not website_requested and not resume_requested:
            print(
                "Must specify --website, --resume, --all, or a resume "
                "artifact in order to validate."
            )
            sys.exit(1)

        if website_requested:
            schema.website(config['configs']['website'])

        if resume_requested:
            schema.resume(config['configs']['resume'])

        sys.exit(0)

    if args.backup:
        if not website_requested and not resume_requested:
            print(
                "Must specify --website, --resume, or --all "
                "in order to back up templates."
            )
            sys.exit(1)

        if website_requested:
            AleaHelperFunctions.backup_files(
                config['templates']['website']
            )

        if resume_requested:
            AleaHelperFunctions.backup_files(
                config['templates']['resume']
            )

    if website_requested:
        render_website()

    if args.all or args.resume:
        selected_actions = resume_actions
    else:
        selected_actions = (
            artifact
            for artifact in resume_actions
            if getattr(args, artifact)
        )

    selected_actions = tuple(selected_actions)

    if selected_actions:
        schema.resume(config['configs']['resume'])

        for action in selected_actions:
            actions[action]()

if __name__ == "__main__":
    main()
