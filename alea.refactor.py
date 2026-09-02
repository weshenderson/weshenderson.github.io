#!/usr/bin/env python3
"""
 Author: Wes Henderson
 Quickly generate a new website and/or resume assets based off of
 the configs/index.yaml and configs/resume.yaml files respectively.
 Any changes to this file, index.yaml, resume.yaml, or their templates
 will trigger this script at the time of commit (assuming the pre-commit
 hook is in place).

 TODO:
  * Move remaining HTML dependencies to their respective data files.
  * Fix the -s option (broken after migrating to jinga2).
  * Add validation and creation options for CONFIG_FILE.
  * Where possible, integrate PDF operations into Alea.
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

from src_refactor import config
from src_refactor import AleaHelperFunctions
from src_refactor import RenderDocx
from src_refactor import RenderJson
from src_refactor import RenderTemplates
#from src_refactor import RenderDocxMetadata
#from src_refactor import RenderPdfMetadata
from src_refactor import RenderMetadata
from src_refactor import ValidateSchema

# pylint: disable=too-many-statements
def main():
    """Entrypoint for Alea."""

    json          = RenderJson()
    templates     = RenderTemplates()
    docx          = RenderDocx()
    metadata      = RenderMetadata()

    # Create the parser
    description = "Generate a link tree style webpage and/or a resume based off of YAML!"
    epilog = "Copy .hooks/pre-commit to .git/hooks/pre-commit to automatically run on commit."
    job_options = argparse.ArgumentParser(description=description, epilog=epilog)

    # Add the arguments
    job_options.add_argument('-s',
                             '--stdout',
                             default=False,
                             action='store_true',
                             help='Print the content to stdout rather than creating files.')
    job_options.add_argument('-b',
                             '--backup',
                             default=False,
                             action='store_true',
                             help='Create a backup copy of the templated files (-r or -i).')
    job_options.add_argument('-w',
                             '--website',
                             default=False,
                             action='store_true',
                             help='Generate the new website artifacts.')
    job_options.add_argument('-r',
                             '--resume',
                             default=False,
                             action='store_true',
                             help='Build new resume artifacts.')
    job_options.add_argument('-v',
                             '--validate',
                             default=False,
                             action='store_true',
                             help='Validate the yaml schema (must include -r or -i).')
    job_options.add_argument('-p',
                            '--pdf',
                            default=False,
                            action='store_true',
                            help='Apply build metadata to the PDF artifact.')

    args = job_options.parse_args()

    if args.validate and args.website and args.resume:
        ValidateSchema.website_schema()
        ValidateSchema.resume_schema()
        sys.exit(0)
    elif args.validate and args.website:
        ValidateSchema.website_schema()
        sys.exit(0)
    elif args.validate and args.resume:
        ValidateSchema.resume_schema()
        sys.exit(0)
    elif args.validate:
        print('Must specify either -i and/or -r in order to validate the correct schema.')
        sys.exit(1)

    if args.backup and args.website and args.resume:
        AleaHelperFunctions.backup_files(config['templates']['website'])
        AleaHelperFunctions.backup_files(config['templates']['resume'])
    elif args.backup and args.website:
        AleaHelperFunctions.backup_files(config['templates']['website'])
    elif args.backup and args.resume:
        AleaHelperFunctions.backup_files(config['templates']['resume'])
    elif args.backup:
        print('Must specify either -i and/or -r to backup the proper files.')
        sys.exit(1)

    if args.website:
        target = "website"
        ValidateSchema.website_schema()
        templates.render(target, config)

    if args.resume:
        target = "resume"
        ValidateSchema.resume_schema()
        json.render(config['configs'], config['templates']['resume']['json']['destination'])
        templates.render(target, config)
        docx.render(config['templates']['resume']['docx']['destination'])
        docx.validate_resume(config['templates']['resume']['docx']['destination'])
        #docx_metadata.render(config['templates']['resume']['docx']['destination'])
        metadata.render(config['templates']['resume']['docx']['destination'])
        json.render(config['configs'], config['templates']['resume']['json']['destination'])

    if args.pdf:
        #pdf_metadata.render(config['templates']['resume']['pdf']['destination'])
        metadata.render(config['templates']['resume']['pdf']['destination'])

if __name__ == "__main__":
    main()
