"""
File creation: resume(s), website, file backups, etc.
"""

from shutil import copyfile
from string import Template

from os import path, remove

import json
import sys
import yaml

class GenerateFiles:
    """File operations."""

    @staticmethod
    def update_content(content_templates, site_content, stdout):
        """Generate HTML/CSS assets from their templates."""

        for template in content_templates:
            # pylint: disable=unsubscriptable-object
            source = content_templates[template]['source']
            # pylint: disable=unsubscriptable-object
            destination = content_templates[template]['destination']
            try:
                with open(source, 'r', encoding='UTF-8') as file:
                    src = Template(file.read())
                    result = src.substitute(site_content)
                if stdout:
                    print(f'File: {source}\n')
                    print(result)
                else:
                    if path.exists(destination):
                        remove(destination)
                    with open(destination, 'a+', encoding='UTF-8') as dest:
                        dest.write(result)
            except OSError:
                print(f"Unable to access file: {source}")
        if not stdout:
            dir_path = path.dirname(path.realpath(__file__))
            # pylint: disable=unsubscriptable-object
            site_path = 'file://' + dir_path + '/' + content_templates['html']['destination']
            print(f'New site built: {site_path}')

    @staticmethod
    def generate_json():
        """Generate a JSON copy of the resume."""

        resume_yaml = 'configs/resume.yaml'
        resume_json = 'resumes/resume.json'

        print("Generating the JSON version of the resume.")
        with open(resume_yaml, encoding='UTF-8') as file:
            content = yaml.safe_load(file)

        with open(resume_json, 'w', encoding='UTF-8') as file:
            json.dump(content, file, indent=2)

    @staticmethod
    def backup_files(templates):
        """Backup associated files in the current working directory."""

        for template in templates:
            # pylint: disable=unsubscriptable-object
            print(f'Backing up file: {templates[template]["destination"]}')
            # pylint: disable=unsubscriptable-object
            templates[template]['backup'] = f"{templates[template]['destination']}.bak"
            try:
                # pylint: disable=unsubscriptable-object
                copyfile(templates[template]['destination'], templates[template]['backup'])
            except OSError:
                print(f'Unable to openfile: {templates[template]["destination"]}')
                sys.exit(5)
