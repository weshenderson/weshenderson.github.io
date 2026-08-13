"""
Build website object.
"""

from datetime import date
import yaml

from .analytics import Analytics
from .schema import SchemaValidations

# pylint: disable=too-few-public-methods
class BuildWebsite:
    """Website operations."""

    INDEX   = 'configs/index.yaml'

    def build_index_object(self) -> dict:
        """Convert index.yaml into a dictionary."""

        # Validate Schema.
        SchemaValidations.index_schema()

        with open(self.INDEX, encoding='UTF-8') as file:
            content = yaml.safe_load(file)

        today = date.today()
        year = today.year

        # Initialize site_content.
        site_content = {
            'author': content['meta']['siteAuthor'],
            'description': content['meta']['siteDescription'],
            'icon': content['meta']['siteIcon'],
            'tags': ','.join(content['meta']['siteTags']),
            'image': content['content']['heroImage']['path'],
            'alt': content['content']['heroImage']['altText'],
            'header': ''.join(f'<p>{line}</p>'
                            for line in content['content']['header']),
            'body': ''.join(f'<a target="_blank" href="{link}">{site}</a><br>'
                            for site, link in content['content']['body'].items()),
            'footer': '',
            'background': content['pageLayout']['color']['background'],
            'font_color': content['pageLayout']['color']['font'],
            'link': content['pageLayout']['color']['clickedLink'],
            'font': content['pageLayout']['font']['name'],
            'font_size_primary': content['pageLayout']['font']['size'],
            'font_size_secondary': content['pageLayout']['font']['size'] / 2,
            'google_font': ''
        }

        # Grab the footer(s).
        count = 1
        for entry in content['content']['footer']:
            if not entry['combineTitle']:
                site_content['footer'] += f'<p>{entry["title"]}</p>'
            else:
                delimiter = entry['fs']
                site_content['footer'] += f'<p>{entry["title"]}'
                for label, link in entry['links'].items():
                    if count < len(entry['links']):
                        site_content['footer'] += f'<a target="_blank" href="' \
                                                f'{link}">{label}</a> {delimiter} '
                        count += 1
                    else:
                        site_content['footer'] += f'<a target="_blank" href="' \
                                                f'{link}">{label}</a></p>'
        if content['content']['copyright']:
            site_content['footer'] += f'<p>© {year} {site_content["author"]}</p>'

        # Set a Google font.
        if content['pageLayout']['font']['googleFont']:
            site_content['google_font'] = content['pageLayout']['font']['fontLink']
            print('** Google fonts are not yet implemented. **')

        # Build Google Analytics.
        Analytics.build_analytics(content, site_content)

        return site_content
