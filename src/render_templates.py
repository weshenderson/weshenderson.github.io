"""
Render jinga2 templates.
"""

import datetime

import yaml
from jinja2 import Environment, FileSystemLoader

# pylint: disable=too-few-public-methods
class RenderTemplates:
    """Render templates."""

    def render(self, target, config):
        """Generate HTML/CSS assets from template(s)."""

        templates_dir  = config['configs']['templatesDir']
        website_config = config['configs']['website']
        resume_config  = config['configs']['resume']

        env = Environment(
            loader=FileSystemLoader(templates_dir),
            autoescape=True
            )

        if target == "website":
            templates = config['templates']['website']

            for _, paths in templates.items():
                with open(website_config, encoding='UTF-8') as web_config_file:
                    data = yaml.safe_load(web_config_file)

                template = env.get_template(paths['source'])
                content  = template.render(**data, current_year=datetime.datetime.now().year)

                with open(paths['destination'], 'w', encoding='UTF-8') as dest:
                    dest.write(content)

        elif target == "resume":
            templates = config['templates']['resume']

            for _, paths in templates.items():
                with open(resume_config, encoding='UTF-8') as resume_config_file:
                    data = yaml.safe_load(resume_config_file)

                try:
                    template = env.get_template(paths['source'])
                except AttributeError:
                    continue

                content  = template.render(**data, current_year=datetime.datetime.now().year)

                with open(paths['destination'], 'w', encoding='UTF-8') as dest:
                    dest.write(content)
