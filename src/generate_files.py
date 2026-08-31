"""
File creation: resume(s), website, file backups, etc.
"""

from shutil import copyfile
from pathlib import Path
import datetime

import json
import sys
import yaml
from jinja2 import Environment, FileSystemLoader

from .schema import SchemaValidations

INDEX_YAML  = 'configs/index.yaml'
RESUME_YAML = 'configs/resume.yaml'
RESUME_JSON = 'resumes/resume.json'
BUILD_DATA  = 'templates/.build.metadata'

class GenerateFiles:
    """File operations."""

    @staticmethod
    def update_content(target, templates_dir, templates):
        """Generate HTML/CSS assets from template(s)."""

        env = Environment(
            loader=FileSystemLoader(templates_dir),
            autoescape=True
            )

        if target == "website":
            SchemaValidations.index_schema()

            for _, paths in templates.items():
                with open(INDEX_YAML, encoding='UTF-8') as config:
                    data = yaml.safe_load(config)

                template = env.get_template(paths['source'])
                content  = template.render(**data, current_year=datetime.datetime.now().year)

                with open(paths['destination'], 'w', encoding='UTF-8') as dest:
                    dest.write(content)
        elif target == "resume":
            SchemaValidations.resume_schema()

            for _, paths in templates.items():
                with open(RESUME_YAML, encoding='UTF-8') as config:
                    data = yaml.safe_load(config)

                try:
                    template = env.get_template(paths['source'])
                except AttributeError:
                    continue

                content  = template.render(**data, current_year=datetime.datetime.now().year)

                with open(paths['destination'], 'w', encoding='UTF-8') as dest:
                    dest.write(content)


    @staticmethod
    def generate_json():
        """Generate a JSON copy of the resume with optional build data."""

        SchemaValidations.resume_schema()

        build_data = GenerateFiles.read_build_info(BUILD_DATA)

        print("Generating the JSON version of the resume.")
        with open(RESUME_YAML, encoding='UTF-8') as file:
            content = yaml.safe_load(file)

        if build_data:
            content.setdefault("meta", {})
            content["meta"]["buildData"] = build_data

        with open(RESUME_JSON, 'w', encoding='UTF-8') as file:
            json.dump(content, file, indent=2)

    @staticmethod
    def read_build_info(build_data_file):
        """Read build information from an optional metadata file."""

        metadata_file = Path(build_data_file)

        if not metadata_file.is_file():
            return None

        build_data = {}

        with metadata_file.open(encoding="UTF-8") as file:
            build_data = yaml.safe_load(file)

        return {"buildData": build_data}

    @staticmethod
    def backup_files(templates):
        """Backup associated files."""

        for _, paths in templates.items():
            src  = paths["destination"]
            dest = f'{paths["destination"]}.bak'
            print(f'Backing up file: {src}')

            try:
                copyfile(src, dest)
            except OSError:
                print(f'Unable to openfile: {src}')
                sys.exit(5)
