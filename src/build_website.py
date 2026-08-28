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

    INDEX = 'configs/index.yaml'

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
            'site_description': content['meta']['siteDescription'],
            'icon': content['meta']['siteIcon'],
            'tags': ','.join(content['meta']['siteTags']),
            'image': content['content']['heroImage']['path'],
            'alt': content['content']['heroImage']['altText'],
            'header': content['content']['header'],
            'resume': content['content']['resume'],
            'links': ''.join(f'<li><a target="_blank" rel="noopener" href="{link}">{site}</a></li>'
                            for site, link in content['content']['links'].items()),
            'prompt': content['content']['prompt'],
            'name': content['content']['name'],
            'description': content['content']['description'],
            'title': content['content']['title'],
            'site': content['content']['site'],
            'pid': content['content']['pid'],
            'sys_info': '',
            'sys_info_heading': content['content']['system-info']['heading'],
            'sys_info_content': ''.join(f'<tr><td>{field}:</td><td>{status}</td></tr>'
                                       for field, status in \
                                        content['content']['system-info']['table'].items()),
            'footer': '',
            'background': content['pageLayout']['color']['background'],
            'primary': content['pageLayout']['color']['primary'],
            'secondary': content['pageLayout']['color']['secondary'],
            'tertiary': content['pageLayout']['color']['tertiary'],
            'font_color': content['pageLayout']['color']['font'],
            'link': content['pageLayout']['color']['clickedLink'],
            'font': content['pageLayout']['font']['name'],
            'font_size_primary': content['pageLayout']['font']['size'],
            'font_size_secondary': content['pageLayout']['font']['size'] / 2,
            'google_font': ''
        }

        # Build the sys-info table.
        if not content['content']['system-info']['enable']:
            site_content['sys_info'] = ""
        else:
            site_content['sys_info'] += '<table class="system-info">'
            site_content['sys_info'] += f'<tr><th colspan="2">\
                                          {site_content["sys_info_heading"]}</th></tr>'
            site_content['sys_info'] += site_content['sys_info_content']
            site_content['sys_info'] += '</table>'

        # Build the footer.
        if content['content']['copyright']:
            site_content['footer'] += f'<p>Connection to {site_content["site"]} closed.\
                                        <br>© {year} {site_content["author"]}.<br>\
                                        All rights reserved.</p>'
        else:
            site_content['footer'] += f'<p>Connection to {site_content["site"]} closed.</p>'

        count = 1
        for entry in content['content']['footer']:
            if not entry['combineTitle']:
                site_content['footer'] += f'<p class="donations">{entry["title"]}</p>'
            else:
                delimiter = entry['fs']
                site_content['footer'] += f'<p class="donations">{entry["title"]}'
                for label, link in entry['links'].items():
                    if count < len(entry['links']):
                        site_content['footer'] += f'<a target="_blank" rel="noopener \
                                                    noreferrer" href="' \
                                                  f'{link}">{label}</a> {delimiter} '
                        count += 1
                    else:
                        site_content['footer'] += f'<a target="_blank" rel="noopener noreferrer"\
                                                    href="' \
                                                  f'{link}">{label}</a></p>'

        # Set a Google font.
        if content['pageLayout']['font']['googleFont']:
            site_content['google_font'] = content['pageLayout']['font']['fontLink']
            print('** Google fonts are not yet implemented. **')

        # Build Google Analytics.
        Analytics.build_analytics(content, site_content)

        return site_content
