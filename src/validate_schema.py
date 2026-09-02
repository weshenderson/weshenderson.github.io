"""
Schema operations: definitions & validations
"""

import sys
import yaml

import schema

class ValidateSchema:
    """Schema definitions and validations."""

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
