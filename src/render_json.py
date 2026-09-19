"""
Render JSON resume from canonical data source.
"""

import json
import yaml

# pylint: disable=too-few-public-methods
class RenderJson:
    """Render JSON resume."""

    def render(self, configs, dest):
        """Generate a JSON copy of the resume."""

        print("Generating the JSON version of the resume.")

        with open(configs['resume'], encoding='UTF-8') as file:
            content = yaml.safe_load(file)

        with open(dest, 'w', encoding='UTF-8') as file:
            json.dump(content, file, indent=2)
