"""
Schema operations: definitions & validations
"""

import json
import sys
import tarfile
from pathlib import Path
from urllib.request import urlopen

import schema
import yaml
from jsonschema import Draft7Validator

class ValidateSchema:
    """Schema definitions and validations."""

    JSON_RESUME_VERSION = "1.3.1"
    JSON_RESUME_SCHEMA_COMMIT = "d8ebc8c816ae15db10f40e0fefaf4c935e025ea1"

    def json_resume(self, json_file):
        """Validate JSON Resume against the JSON Resume schema."""

        schema_path = (
            Path(__file__).parent.parent
            / "schemas"
            / f"jsonresume-{self.JSON_RESUME_VERSION}.json"
        )

        schema_url = (
            "https://raw.githubusercontent.com/"
            "jsonresume/jsonresume.org/"
            f"{self.JSON_RESUME_SCHEMA_COMMIT}/"
            "packages/schema/schema.json"
        )

        if not schema_path.exists():
            print(f"Downloading JSON Resume schema: {schema_path}")

            schema_path.parent.mkdir(parents=True, exist_ok=True)

            try:
                with urlopen(schema_url, timeout=10) as response:
                    schema_path.write_bytes(response.read())
            except (OSError, tarfile.TarError) as error:
                print(f"Unable to download JSON Resume schema: {error}")
                sys.exit(1)

        with open(schema_path, encoding="UTF-8") as file:
            json_schema = json.load(file)

        with open(json_file, encoding="UTF-8") as file:
            resume = json.load(file)

        print(f"Validating JSON Resume schema: {json_file}")

        validator = Draft7Validator(json_schema)

        errors = sorted(
            validator.iter_errors(resume),
            key=lambda error: list(error.absolute_path)
        )

        if errors:
            print(f"JSON Resume validation failed: {json_file}")

            for error in errors:
                path = ".".join(str(part) for part in error.absolute_path)
                location = path if path else "root"
                print(f"{location}: {error.message}")

            sys.exit(1)

        print(f"JSON Resume is valid: {json_file}")

    def website(self, yaml_file):
        """Definition for the website.yaml schema."""

        bool_error = "Unsupported option; must be either true or false."
        config_schema = schema.Schema({
            "meta": {
                "siteAuthor": str,
                "siteDescription": str,
                "siteIcon": str,
                "siteTags": list,
                schema.Optional("googleAnalytics"): schema.Or(str, None)
            },
            "pageLayout": {
                "color": {
                    "background": str,
                    "font": str,
                    "clickedLink": str
                },
                "font": {
                    "googleFont": schema.Or(bool,error=bool_error),
                    "fontLink": str,
                    "name": str,
                    "size": int
                }
            },
            "content": {
                "header": str,
                "heroImage": {
                    "path": str,
                    "altText": str
                },
                "links": dict,
                "donations": dict,
                "copyright": schema.Or(bool, error=bool_error)
            },
        }, ignore_extra_keys=True)

        self.validate_schema(config_schema, yaml_file)

    def resume(self, yaml_file):
        """Definition for the resume.yaml schema."""

        config_schema = schema.Schema({
            "meta": {
                schema.Optional("siteAuthor"): str,
                schema.Optional("siteDescription"): str,
                schema.Optional("siteIcon"): str,
                schema.Optional("siteThumbnail"): str,
                schema.Optional("siteTags"): list,
                schema.Optional("googleAnalytics"): schema.Or(str, None),
                schema.Optional("emailSubject"): schema.Or(str, None)
            },
            "basics": {
                "name": str,
                "label": str,
                "image": str,
                "email": str,
                "phone": str,
                "url": str,
                "summary": str,
                "location": {
                    "city": str,
                    "countryCode": str
                },
                schema.Optional("profiles"): list,
            },
            schema.Optional("skills"): list,
            schema.Optional("work"): list,
            schema.Optional("certificates"): list,
            schema.Optional("education"): list,
        }, ignore_extra_keys=True)

        self.validate_schema(config_schema, yaml_file)

    @staticmethod
    def validate_schema(correct_schema, file):
        """Validate the supplied schema."""

        print(f"Validating schema: {file}")

        with open(file, encoding='UTF-8') as yaml_file:
            content = yaml.safe_load(yaml_file)

        try:
            # pylint: disable=no-member
            correct_schema.validate(content)
            print(f"Configuration is valid: {file}")
        except schema.SchemaError as schema_error:
            for error in schema_error.errors:
                if error:
                    print(error)
            for error in schema_error.autos:
                if error:
                    print(error)
            sys.exit(1)
