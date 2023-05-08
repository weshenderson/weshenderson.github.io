#!/usr/bin/env python3
"""
 Author: Wes Henderson
 Quickly generate a new index.html file based off of content.yaml.
 Any changes to this file, content.yaml, index.tmpl, or associated
 CSS files will trigger this script at the time of commit.

 TODO:
  * Look into alternative templating solutions.
  * Support CLI options for the resume.
    -s
    -b
    -c
  * Create Schema for resume.yaml
  * More verbose output around what is being validated and built.
  * Add checks in case the source files don't exist.
"""

import argparse
import yaml
import schema
from os import path, remove
from shutil import copyfile
from datetime import date
from string import Template

logo = """
 ▄▄▄▄▄▄▄▄▄▄▄  ▄            ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄ 
▐░░░░░░░░░░░▌▐░▌          ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌
▐░█▀▀▀▀▀▀▀█░▌▐░▌          ▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌
▐░▌       ▐░▌▐░▌          ▐░▌          ▐░▌       ▐░▌
▐░█▄▄▄▄▄▄▄█░▌▐░▌          ▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄█░▌
▐░░░░░░░░░░░▌▐░▌          ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌
▐░█▀▀▀▀▀▀▀█░▌▐░▌          ▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌
▐░▌       ▐░▌▐░▌          ▐░▌          ▐░▌       ▐░▌
▐░▌       ▐░▌▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄▄▄ ▐░▌       ▐░▌
▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌       ▐░▌
 ▀         ▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀         ▀ 
"""


def build_content_object():
    """Convert content.yaml into a dictionary."""

    with open('configs/content.yaml') as f:
        content = yaml.safe_load(f)

    today = date.today()
    year = today.year

    # Grab the meta content & hero image.
    site_content = {'author': content['Meta']['Author'], 'description': content['Meta']['Description'],
                    'icon': content['Meta']['Icon'], 'tags': ','.join([tag for tag in content['Meta']['Tags']]),
                    'twitter': content['Meta']['Twitter'], 'image': content['Image']['Path'],
                    'alt': content['Image']['AltText'], 'header': ''}

    # Grab the header(s).
    for title in content['Header']:
        site_content['header'] += '<p>' + content['Header'][title] + '</p>'

    # Grab the body.
    site_content['body'] = ''
    for link in content['Body']:
        site_content['body'] += '<a target="_blank" href="' + content['Body'][link] + '">' + link + '</a><br>'

    # Grab the footer(s).
    count = 1
    site_content['footer'] = ''
    for title in content['Footer']:
        if title != 'Copyright' and title != 'CombinedTitle':
            site_content['footer'] += '<p>' + content['Footer'][title] + '</p>'
    if 'CombinedTitle' in content['Footer']:
        delimiter = content['Footer']['CombinedTitle']['FS']
        site_content['footer'] += '<p>' + content['Footer']['CombinedTitle']['Title']
        for link in content['Footer']['CombinedTitle']['Links']:
            if count < len(content['Footer']['CombinedTitle']['Links']):
                site_content['footer'] += '<a target="_blank" href="' + content['Footer']['CombinedTitle']['Links'][
                    link] + '">' + link + '</a>' + delimiter
                count += 1
            else:
                site_content['footer'] += '<a target="_blank" href="' + content['Footer']['CombinedTitle']['Links'][
                    link] + '">' + link + '</a></p>'
    if content['Footer']['Copyright']:
        site_content['footer'] += f"<p>© {year} {site_content['author']}</p>"

    # Grab the CSS.
    site_content['background'] = content['Page']['Color']['Background']
    site_content['font_color'] = content['Page']['Color']['Font']
    site_content['link'] = content['Page']['Color']['Clicked-Link']
    site_content['font'] = content['Page']['Font']
    if content['Page']['Borders']:
        site_content['borders'] = '2px solid yellow'
    else:
        site_content['borders'] = 'none'

    # Build Google Analytics.
    site_content = build_analytics_object(content, site_content)

    return site_content


def build_resume_object():
    """Convert resume.yaml into a dictionary."""

    with open('configs/resume.yaml') as f:
        content = yaml.safe_load(f)

    # Grab the meta content.
    resume_content = {'author': content['Meta']['Author'], 'description': content['Meta']['Description'],
                      'icon': content['Meta']['Icon'], 'thumbnail': content['Meta']['Thumbnail'],
                      'tags': ','.join([tag for tag in content['Meta']['Tags']]), 'twitter': content['Meta']['Twitter']}

    # Build the Google Analytics object.
    resume_content = build_analytics_object(content, resume_content)

    # Build the resume objects.
    # Overview Info
    resume_content['title'] = content['Contact']['Title']
    resume_content['phone'] = content['Contact']['Phone']
    resume_content['email'] = content['Contact']['Email']

    # Professional Summary
    resume_content['summary'] = content['Summary']

    # Skills
    resume_content['skills'] = ''
    for skill in content['Skills']:
        resume_content['skills'] += '<p>• ' + content['Skills'][skill] + '</p>'

    # Experience
    resume_content['experience'] = ''
    for xp in content['Experience']:
        resume_content['experience'] += '<div class="job"><h2>' + content['Experience'][xp]['Company'] + '</h2><h3>' + \
                                        content['Experience'][xp]['Title'] + '</h3><h4>' + content['Experience'][xp][
                                            'Dates'] + '</h4>' + '<p>• ' + '</p><p>• '.join(
            [s for s in content['Experience'][xp]['Summary']]) + '</p></div>'

    # Certifications
    cert_count = len(content['Certifications'])

    count = 1
    resume_content['certifications'] = '<ul class="talent">'
    for cert in content['Certifications']:
        if count < cert_count:
            resume_content['certifications'] += '<li>' + content['Certifications'][cert]['Title'] + '</li>'
        else:
            resume_content['certifications'] += '<li class="last">' + content['Certifications'][cert]['Title'] + '</li>'
        count += 1
    resume_content['certifications'] += '</ul>'

    count = 1
    resume_content['certifications'] += '<ul class="talent">'
    for cert in content['Certifications']:
        if count < cert_count:
            resume_content['certifications'] += '<li>' + content['Certifications'][cert]['Year'] + '</li>'
        else:
            resume_content['certifications'] += '<li class="last">' + content['Certifications'][cert]['Year'] + '</li>'
        count += 1
    resume_content['certifications'] += '</ul>'

    count = 1
    resume_content['certifications'] += '<ul class="talent">'
    for cert in content['Certifications']:
        if count < cert_count:
            resume_content['certifications'] += '<li>' + content['Certifications'][cert]['License'] + '</li>'
        else:
            resume_content['certifications'] += '<li class="last">' + content['Certifications'][cert][
                'License'] + '</li>'
        count += 1
    resume_content['certifications'] += '</ul>'

    # Education
    resume_content['education'] = ''
    for school in content['Education']:
        resume_content['education'] += '<h2>' + content['Education'][school]['School'] + ' - ' + \
                                       content['Education'][school]['Location'] + '</h2><h3>' + \
                                       content['Education'][school]['Degree']
        if content['Education'][school]['GPA']:
            resume_content['education'] += ' &mdash; <strong>' + content['Education'][school][
                'GPA'] + ' GPA</strong></h3>'
        else:
            resume_content['education'] += '</h3>'
        if content['Education'][school]['Achievements']:
            resume_content['education'] += '<p>• ' + '</p><p>• '.join(
                [a for a in content['Education'][school]['Achievements']]) + '</p>'

    return resume_content


def build_analytics_object(config_file, content_object):
    """Build Google Analytics and append to the dictionary. Not yet implemented."""
    if config_file['Google']['Analytics']:
        content_object['google_id'] = config_file['Google']['ID']
        content_object['google'] = """
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=$google_id"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());

      gtag('config', '$google_id');
    </script>"""

        content_object['google'] = Template(content_object['google'])
        content_object['google'] = content_object['google'].substitute(content_object)
    else:
        content_object['google'] = ''
    return content_object


def build_assets(source, destination, site_content, index):
    """Generate HTML/CSS assets from their templates."""

    if index:
        if path.exists(destination):
            remove(destination)
    with open(source, 'r') as f:
        src = Template(f.read())
        result = src.substitute(site_content)
    if index:
        with open(destination, 'a+') as d:
            d.write(result)
    else:
        print(result)
    return


def build_resume(source, destination, resume_content, resume):
    """Generate HTML/CSS assets from their templates."""

    if resume:
        if path.exists(destination):
            remove(destination)
    with open(source, 'r') as f:
        src = Template(f.read())
        result = src.substitute(resume_content)
    if resume:
        with open(destination, 'a+') as d:
            d.write(result)
    else:
        print(result)
    return


def check_schema():
    """Validate the content.yaml schema."""

    config_schema = schema.Schema({
        "Meta": {
            "Author": str,
            "Description": str,
            "Icon": str,
            "Twitter": str,
            "Tags": list
        },
        "Google": {
            "Analytics": bool,
            schema.Optional("ID"): schema.Or(str, None)
        },
        "Page": {
            "Color": {
                "Background": str,
                "Font": str,
                "Clicked-Link": str
            },
            "Font": str,
            "Borders": bool
        },
        "Header": {
            "Title": str
        },
        "Image": {
            "Path": str,
            "AltText": str
        },
        "Body": {
            schema.Optional(object): object
        },
        "Footer": {
            schema.Optional("Title"): schema.Or(str, None),
            schema.Optional("CombinedTitle"): {
                schema.Optional(object): object
            },
            "Copyright": schema.Or(bool, error="Unsupported option. Copyright must be either True or False.")
        }
    }, ignore_extra_keys=True)
    print("Validating schema.")

    with open('configs/content.yaml') as f:
        content = yaml.safe_load(f)

    try:
        config_schema.validate(content)
        print("Configuration is valid.")
    except schema.SchemaError as se:
        for error in se.errors:
            if error:
                print(error)
        for error in se.autos:
            if error:
                print(error)
        exit(1)
    return


def main():
    """Entrypoint for site_generator."""

    print(logo)

    # Create the parser
    description = "Automatically generate a link tree style webpage based off of content.yaml!"
    epilog = "If this file is not being automatically executed, copy .hooks/pre-commit to .git/hooks/pre-commit."
    job_options = argparse.ArgumentParser(description=description, epilog=epilog)

    # Add the arguments
    job_options.add_argument('-s',
                             '--stdout',
                             default=False,
                             action='store_true',
                             help='Print the index.html to stdout. -- Not yet implemented for resume.')
    job_options.add_argument('-b',
                             '--backup',
                             default=False,
                             action='store_true',
                             help='Create a backup copy of the templated files. -- Not yet implemented for resume.')
    job_options.add_argument('-i',
                             '--index',
                             default=False,
                             action='store_true',
                             help='Generate the new index.html assets.')
    job_options.add_argument('-r',
                             '--resume',
                             default=False,
                             action='store_true',
                             help='Generate the new resume.html assets.')
    job_options.add_argument('-c',
                             '--check',
                             default=False,
                             action='store_true',
                             help='Validate the content.yaml file only. -- Not yet implemented for resume.')

    args = job_options.parse_args()
    stdout = args.stdout
    backup = args.backup
    index = args.index
    resume = args.resume
    check = args.check

    check_schema()
    if check:
        exit(0)

    site_content = build_content_object()
    content_templates = dict(html={'source': 'templates/index.tmpl',
                                   'destination': 'index.html',
                                   }, css={'source': 'templates/css.tmpl',
                                           'destination': 'assets/css/main.css',
                                           })
    resume_templates = dict(html={'source': 'templates/srt-resume.tmpl',
                                  'destination': 'resume.html',
                                  }, konami={'source': 'templates/srt-konami-resume.tmpl',
                                             'destination': 'konami-resume.html'
                                             })

    if backup:
        print('Backing up the files.')
        for template in content_templates:
            content_templates[template]['backup'] = f"{content_templates[template]['destination']}.bak"
            copyfile(content_templates[template]['destination'], content_templates[template]['backup'])
    if stdout:
        print('Printing the generated files to stdout only.\n')
        for template in content_templates:
            source = content_templates[template]['source']
            destination = content_templates[template]['destination']
            print("File: {}\n".format(destination))

            build_assets(source, destination, site_content, index)
    elif index:
        print('Generating the new assets.')

        for template in content_templates:
            source = content_templates[template]['source']
            destination = content_templates[template]['destination']

            build_assets(source, destination, site_content, index)

        dir_path = path.dirname(path.realpath(__file__))
        site_path = 'file://' + dir_path + '/' + content_templates['html']['destination']
        print(f'New site built: {site_path}')

    if resume:
        resume_content = build_resume_object()

        for template in resume_templates:
            source = resume_templates[template]['source']
            destination = resume_templates[template]['destination']

            build_resume(source, destination, resume_content, resume)

    return


if __name__ == "__main__":
    main()
