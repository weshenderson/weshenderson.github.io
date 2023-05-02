#!/usr/bin/env python3
"""
 Author: Wes H.
 Quickly generate a new index.html file based off of content.yaml.
 Any changes to this file, content.yaml, index.tmpl, or associated
 CSS files will trigger this script at the time of commit.

 TODO:
  * Break out the functions and add documentation.
  * Reduce/Remove HTML from this file.
  * Look into alternative templating solutions.
  * Make '529' a more universial heading.
"""

import os
import sys
import yaml
from datetime import date
from string import Template

def build_assets(source, destination, site_content):
    if os.path.exists(destination):
        os.remove(destination)
    with open(source, 'r') as f:
        src    = Template(f.read())
        result = src.substitute(site_content)
        with open(destination, 'a+') as d:
            d.write(result)
    return

def main():
    """Convert content.yaml into a dictionary and create index.html from index.tmpl."""
    with open('content.yaml') as f:
        content = yaml.safe_load(f)

    site_content = {}
    templates    = {'html':
                     {'source': 'templates/index.tmpl',
                      'destination': 'index.html',
                     },
                    'css':
                     {'source': 'templates/css.tmpl',
                      'destination': 'assets/css/main.css',
                     },
                   }
    today        = date.today()
    year         = today.year

    ## Generate the meta content.
    site_content['author']      = content['Meta']['Author']
    site_content['description'] = content['Meta']['Description']
    site_content['icon']        = content['Meta']['Icon']
    site_content['tags']        = ','.join([tag for tag in content['Meta']['Tags']])
    site_content['twitter']     = content['Meta']['Twitter']

    ## Generate the site image.
    site_content['image'] = content['Image']['Path']
    site_content['alt']   = content['Image']['AltText']

    # Generate the header.
    site_content['header'] = ''
    for title in content['Header']:
        site_content['header'] += '<p>' + content['Header'][title] + '</p>'

    # Generate the body.
    site_content['body'] = ''
    for link in content['Body']:
        site_content['body'] += '<a target="_blank" href="' + content['Body'][link] + '">' + link + '</a><br>'

    # Generate the footer.
    site_content['college'] = '529 Donation Links: '
    count = 1

    for child in content['Footer'][529]:
        if count != len(content['Footer'][529]):
            site_content['college'] += '<a target="_blank" href="' + content['Footer'][529][child] + '">' + child + '</a>' + content['Footer']['FS']
        else:
            site_content['college'] += '<a target="_blank" href="' + content['Footer'][529][child] + '">' + child + '</a>'
        count += 1

    if content['Footer']['Copyright']:
        site_content['college'] += f"<p>© {year} {site_content['author']}</p>"

    # Generate the CSS.
    site_content['background'] = content['Page']['Color']['Background']
    site_content['font_color'] = content['Page']['Color']['Font']
    site_content['link']       = content['Page']['Color']['Clicked-Link']
    site_content['font']       = content['Page']['Font']

    for template in templates:
        source      = templates[template]['source']
        destination = templates[template]['destination']
        build_assets(source, destination, site_content)

if __name__ == "__main__":
    main()
