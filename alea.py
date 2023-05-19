#!/usr/bin/env python3
"""
 Author: Wes Henderson
 Quickly generate a new index.html and/or resume.html based off of
 the configs/content.yaml and configs/resume.yaml files respectively.
 Any changes to this file, content.yaml, resume.yaml, or their templates
 will trigger this script at the time of commit (assuming the pre-commit
 hook is in place).

 TODO:
  * Look into alternative templating solutions.
"""

import argparse
import sys
from datetime import date
from os import path, remove
from shutil import copyfile
from string import Template
import schema
import yaml

LOGO = """
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


def build_index_object():
    """Convert content.yaml into a dictionary."""

    with open('configs/content.yaml', encoding='UTF-8') as file:
        content = yaml.safe_load(file)

    today = date.today()
    year = today.year

    # Grab the meta content & hero image.
    site_content = {'author': content['Meta']['Author'],
                    'description': content['Meta']['Description'],
                    'icon': content['Meta']['Icon'],
                    'tags': ','.join([tag for tag in content['Meta']['Tags']]),
                    'twitter': content['Meta']['Twitter'],
                    'image': content['Image']['Path'],
                    'alt': content['Image']['AltText'], 'header': ''}

    # Grab the header(s).
    for title in content['Header']:
        site_content['header'] += '<p>' + content['Header'][title] + '</p>'

    # Grab the body.
    site_content['body'] = ''
    for link in content['Body']:
        site_content['body'] += '<a target="_blank" href="' + \
                                content['Body'][link] + '">' + link + '</a><br>'

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
                site_content['footer'] += '<a target="_blank" href="' + \
                                          content['Footer']['CombinedTitle']['Links'][
                    link] + '">' + link + '</a>' + delimiter
                count += 1
            else:
                site_content['footer'] += '<a target="_blank" href="' + \
                                          content['Footer']['CombinedTitle']['Links'][
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

    with open('configs/resume.yaml', encoding='UTF-8') as file:
        content = yaml.safe_load(file)

    # Grab the meta content.
    resume_content = {'author': content['Meta']['Author'],
                      'description': content['Meta']['Description'],
                      'icon': content['Meta']['Icon'],
                      'thumbnail': content['Meta']['Thumbnail'],
                      'tags': ','.join([tag for tag in content['Meta']['Tags']]),
                      'twitter': content['Meta']['Twitter']}

    # Build the Google Analytics object.
    resume_content = build_analytics_object(content, resume_content)

    # Build the resume objects.
    # Overview Info
    resume_content['title'] = content['Contact']['Title']
    resume_content['phone'] = content['Contact']['Phone']
    resume_content['email'] = content['Contact']['Email']
    if 'Subject' in content['Contact']:
        resume_content['subject'] = '?subject='
        resume_content['subject'] += content['Contact']['Subject']
    else:
        resume_content['subject'] = ''

    # Professional Summary
    resume_content['summary'] = content['Summary']

    # Skills
    rows = 0
    resume_content['skills'] = ''
    for column in content['Skills']:
        if len(content['Skills'][column]) > rows:
            rows = len(content['Skills'][column])

    for column in content['Skills']:
        count = 0
        resume_content['skills'] += '<ul class="talent">'
        for skill in content['Skills'][column]:
            count += 1
            if count == rows:
                resume_content['skills'] += '<li class="last">' + skill + "</li>"
            else:
                resume_content['skills'] += "<li>" + skill + "</li>"
        resume_content['skills'] += "</ul>"

    # Experience
    resume_content['experience'] = ''
    for exp in content['Experience']:
        resume_content['experience'] += '<div class="job"><h2>' + \
                                        content['Experience'][exp]['Company'] + '</h2><h3>' + \
                                        content['Experience'][exp]['Title'] + '</h3><h4>' + \
                                        content['Experience'][exp]['Dates'] + '</h4>' + '<p>• ' + \
                                        '</p><p>• '.join(
                                            [s for s in content['Experience'][exp]['Summary']]) \
                                        + '</p></div>'

    # Certifications
    cert_count = len(content['Certifications'])

    count = 1
    resume_content['certifications'] = '<ul class="talent">'
    for cert in content['Certifications']:
        if count < cert_count:
            resume_content['certifications'] += '<li>' + \
                                                content['Certifications'][cert]['Title'] + '</li>'
        else:
            resume_content['certifications'] += '<li class="last">' + \
                                                content['Certifications'][cert]['Title'] + '</li>'
        count += 1
    resume_content['certifications'] += '</ul>'

    count = 1
    resume_content['certifications'] += '<ul class="talent-center">'
    for cert in content['Certifications']:
        if count < cert_count:
            resume_content['certifications'] += '<li>' + \
                                                content['Certifications'][cert]['Year'] + '</li>'
        else:
            resume_content['certifications'] += '<li class="last">' + \
                                                content['Certifications'][cert]['Year'] + '</li>'
        count += 1
    resume_content['certifications'] += '</ul>'

    count = 1
    resume_content['certifications'] += '<ul class="talent">'
    for cert in content['Certifications']:
        if count < cert_count:
            resume_content['certifications'] += '<li>' + \
                                                content['Certifications'][cert]['License'] + '</li>'
        else:
            resume_content['certifications'] += '<li class="last">' + \
                                                content['Certifications'][cert]['License'] + '</li>'
        count += 1
    resume_content['certifications'] += '</ul>'

    # Education
    resume_content['education'] = ''
    for school in content['Education']:
        resume_content['education'] += '<h2>' + content['Education'][school]['School'] + ' - ' + \
                                       content['Education'][school]['Location'] + '</h2><h3>' + \
                                       content['Education'][school]['Degree']
        if 'GPA' in content['Education'][school]:
            resume_content['education'] += ' &mdash; <strong>' + content['Education'][school][
                'GPA'] + ' GPA</strong></h3>'
        else:
            resume_content['education'] += '</h3>'
        if 'Achievements' in content['Education'][school]:
            resume_content['education'] += '<p>• ' + '</p><p>• '.join(
                [a for a in content['Education'][school]['Achievements']]) + '</p>'

    return resume_content


def build_analytics_object(config_file, content_object):
    """Build Google Analytics and append to the dictionary."""
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


def backup_files(templates):
    """Backup associated files in the current working directory."""
    for template in templates:
        print(f'Backing up file: {templates[template]["destination"]}')
        templates[template]['backup'] = f"{templates[template]['destination']}.bak"
        try:
            copyfile(templates[template]['destination'], templates[template]['backup'])
        except OSError:
            print(f'Unable to openfile: {templates[template]["destination"]}')
            sys.exit(5)


def update_content(content_templates, site_content, stdout):
    """Generate HTML/CSS assets from their templates."""

    for template in content_templates:
        source = content_templates[template]['source']
        destination = content_templates[template]['destination']
        try:
            with open(source, 'r', encoding='UTF-8') as file:
                src = Template(file.read())
                result = src.substitute(site_content)
            if stdout:
                print(f'File: {source}\n')
                print(result)
            else:
                if path.exists(destination):
                    remove(destination)
                with open(destination, 'a+', encoding='UTF-8') as dest:
                    dest.write(result)
        except OSError:
            print(f"Unable to access file: {source}")
    if not stdout:
        dir_path = path.dirname(path.realpath(__file__))
        site_path = 'file://' + dir_path + '/' + content_templates['html']['destination']
        print(f'New site built: {site_path}')


def index_schema():
    """Definition for the content.yaml schema."""

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
            "Copyright": schema.Or(bool, error="Unsupported option; must be either True or False.")
        }
    }, ignore_extra_keys=True)

    validate_schema(config_schema, file='content.yaml')


def resume_schema():
    """Definition for the resume.yaml schema."""

    config_schema = schema.Schema({
        "Meta": {
            "Author": str,
            "Description": str,
            "Icon": str,
            "Thumbnail": str,
            "Twitter": str,
            "Tags": list
        },
        "Google": {
            "Analytics": bool,
            schema.Optional("ID"): schema.Or(str, None)
        },
        "Contact": {
            "Title": str,
            "Phone": str,
            "Email": str,
            schema.Optional("Subject"): str
        },
        "Summary": str,
        "Skills": {
            1: list,
            2: list
        },
        "Experience": {
            1: {
                "Company": str,
                "Title": str,
                "Dates": str,
                "Summary": list,
            },
            schema.Optional(2): {
                "Company": str,
                "Title": str,
                "Dates": str,
                "Summary": list,
            },
            schema.Optional(3): {
                "Company": str,
                "Title": str,
                "Dates": str,
                "Summary": list,
            },
        },
        "Certifications": {
            1: {
                "Title": str,
                "Year": str,
                "License": str,
            },
        },
        "Education": {
            1: {
                "School": str,
                "Location": str,
                "Degree": str,
                schema.Optional("GPA"): str,
                schema.Optional("Achievements"): list,
            }
        },
    }, ignore_extra_keys=True)

    validate_schema(config_schema, file='resume.yaml')


def validate_schema(correct_schema, file):
    """Validate the supplied schema."""
    print(f"Validating schema: {file}")

    with open(f'configs/{file}', encoding='UTF-8') as yaml_file:
        content = yaml.safe_load(yaml_file)

    try:
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


def main():
    """Entrypoint for Alea."""

    print(LOGO)

    # Create the parser
    description = "Generate a link tree style webpage and/or a resume based off of YAML!"
    epilog = "Copy .hooks/pre-commit to .git/hooks/pre-commit to automatically run on commit."
    job_options = argparse.ArgumentParser(description=description, epilog=epilog)

    # Add the arguments
    job_options.add_argument('-s',
                             '--stdout',
                             default=False,
                             action='store_true',
                             help='Print the content to stdout rather than creating files.')
    job_options.add_argument('-b',
                             '--backup',
                             default=False,
                             action='store_true',
                             help='Create a backup copy of the templated files (-r or -i).')
    job_options.add_argument('-i',
                             '--index',
                             default=False,
                             action='store_true',
                             help='Generate the new index.html and assets.')
    job_options.add_argument('-r',
                             '--resume',
                             default=False,
                             action='store_true',
                             help='Generate the new resume.html and assets.')
    job_options.add_argument('-c',
                             '--check',
                             default=False,
                             action='store_true',
                             help='Validate the yaml schema (must include -r or -i).')

    args = job_options.parse_args()
    stdout = args.stdout
    backup = args.backup
    index = args.index
    resume = args.resume
    check = args.check

    index_templates = {'html': {'source': 'templates/index.tmpl',
                                'destination': 'index.html',
                                }, 'css': {'source': 'templates/css.tmpl',
                                           'destination': 'assets/css/main.css',
                                           }}
    resume_templates = {'html': {'source': 'templates/srt-resume.tmpl',
                                 'destination': 'resume.html',
                                 }, 'konami': {'source': 'templates/srt-konami-resume.tmpl',
                                               'destination': 'konami-resume.html'
                                               }}

    if check and index and resume:
        index_schema()
        resume_schema()
        sys.exit(0)
    elif check and index:
        index_schema()
        sys.exit(0)
    elif check and resume:
        resume_schema()
        sys.exit(0)
    elif check:
        print('Must specify either -i and/or -r in order to validate the correct schema.')
        sys.exit(1)

    if backup and index and resume:
        backup_files(index_templates)
        backup_files(resume_templates)
    elif backup and index:
        backup_files(index_templates)
    elif backup and resume:
        backup_files(resume_templates)
    elif backup:
        print('Must specify either -i and/or -r to backup the proper files.')
        sys.exit(1)

    if index:
        index_schema()
        site_content = build_index_object()
        update_content(index_templates, site_content, stdout)
    if resume:
        resume_schema()
        resume_content = build_resume_object()
        update_content(resume_templates, resume_content, stdout)


if __name__ == "__main__":
    main()
