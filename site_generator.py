#!/usr/bin/env python3

import os
import sys
import yaml
from string import Template

with open('content.yaml') as f:
    content = yaml.safe_load(f)

site_content = {}
source       = 'index.tmpl'
destination  = 'index.html'

## Generate the meta content.
site_content['author']      = content['Meta']['Author']
site_content['description'] = content['Meta']['Description']
site_content['tags']        = ','.join([tag for tag in content['Meta']['Tags']])

# Generate the header.
for title in content['Header']:
    site_content['header'] = content['Header'][title]

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
    site_content['copyright'] = content['Footer']['Copyright']

# Build index.html
if os.path.exists(destination):
    os.remove(destination)
with open(source, 'r') as f:
    src    = Template(f.read())
    result = src.substitute(site_content)
    with open(destination, 'a+') as d:
        d.write(result)

os.chmod(destination, 0o755)
