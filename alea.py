#!/usr/bin/env python3
"""
 Author: Wes Henderson
 Quickly generate a new index.html and/or resume.html based off of
 the configs/index.yaml and configs/resume.yaml files respectively.
 Any changes to this file, index.yaml, resume.yaml, or their templates
 will trigger this script at the time of commit (assuming the pre-commit
 hook is in place).

 TODO:
  * Move remaining HTML dependencies to their respective data files.
  * Fix the -s option (broken after migrating to jinga2).
  * Offload PDF build to GitHub Actions.
  * Expand hooks.
  * Implement artifact provenance.
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

from src import GenerateFiles
from src import SchemaValidations
from src import MachineResume

def main():
    """Entrypoint for Alea."""

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
    job_options.add_argument('-i',
                             '--index',
                             default=False,
                             action='store_true',
                             help='Generate the new index.html and assets.')
    job_options.add_argument('-r',
                             '--resume',
                             default=False,
                             action='store_true',
                             help='Build new resume assets.')
    job_options.add_argument('-j',
                             '--json',
                             default=False,
                             dest="json_resume",
                             action='store_true',
                             help='Generate the JSON resume copy.')
    job_options.add_argument('-c',
                             '--check',
                             default=False,
                             action='store_true',
                             help='Validate the yaml schema (must include -r or -i).')

    args = job_options.parse_args()

    templates_dir   = 'templates'
    website_templates = {'html': {
                            'source': 'index.html',
                            'destination': 'index.html'},
                        'css': {
                            'source': 'main.css',
                            'destination': 'assets/css/main.css'}
                        }

    resume_templates = {'html': {
                            'source': 'resume.html',
                            'destination': 'resumes/resume.html'},
                        'docx': {
                            'source': False,
                            'destination': 'resumes/resume.docx'},
                        'md': {
                            'source': 'resume.md.j2',
                            'destination': 'resumes/resume.md'},
                        }

    if args.check and args.index and args.resume:
        SchemaValidations.index_schema()
        SchemaValidations.resume_schema()
        sys.exit(0)
    elif args.check and args.index:
        SchemaValidations.index_schema()
        sys.exit(0)
    elif args.check and args.resume:
        SchemaValidations.resume_schema()
        sys.exit(0)
    elif args.check:
        print('Must specify either -i and/or -r in order to validate the correct schema.')
        sys.exit(1)

    if args.backup and args.index and args.resume:
        GenerateFiles.backup_files(website_templates)
        GenerateFiles.backup_files(resume_templates)
    elif args.backup and args.index:
        GenerateFiles.backup_files(website_templates)
    elif args.backup and args.resume:
        GenerateFiles.backup_files(resume_templates)
    elif args.backup:
        print('Must specify either -i and/or -r to backup the proper files.')
        sys.exit(1)

    if args.index:
        target = "website"
        GenerateFiles.update_content(target, templates_dir, website_templates)
    if args.resume:
        target = "resume"
        GenerateFiles.update_content(target, templates_dir, resume_templates)
        MachineResume.generate_docx_resume(resume_templates['docx']['destination'])
        MachineResume.validate_docx_resume(resume_templates['docx']['destination'])
    if args.json_resume:
        GenerateFiles.generate_json()

if __name__ == "__main__":
    main()
