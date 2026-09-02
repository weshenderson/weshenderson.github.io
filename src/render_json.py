"""
Render JSON resume from canonical data source.
"""

import json
import yaml

from .alea_helper_functions import AleaHelperFunctions

# pylint: disable=too-few-public-methods
class RenderJson:
    """Render JSON resume."""

    def render(self, configs, dest):
        """Generate a JSON copy of the resume with optional build data."""

        build_data = AleaHelperFunctions.read_build_info(configs['buildData'])

        print("Generating the JSON version of the resume.")
        with open(configs['resume'], encoding='UTF-8') as file:
            content = yaml.safe_load(file)

        if build_data:
            content.setdefault("meta", {})
            content["meta"].update(build_data["meta"])

        with open(dest, 'w', encoding='UTF-8') as file:
            json.dump(content, file, indent=2)
