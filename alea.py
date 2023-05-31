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
  * Make meta sections optional.
  * Expand education schema.
"""

import argparse
import json
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
INDEX = 'configs/content.yaml'
RESUME_YAML = 'configs/resume.yaml'
RESUME_JSON = 'configs/resume.json'


def build_index_object():
    """Convert content.yaml into a dictionary."""

    with open(INDEX, encoding='UTF-8') as file:
        content = yaml.safe_load(file)

    today = date.today()
    year = today.year

    # Initialize site_content.
    site_content = {'author': content['meta']['Author'],
                    'description': content['meta']['Description'],
                    'icon': content['meta']['Icon'],
                    'tags': ','.join(list(content['meta']['Tags'])),
                    'twitter': content['meta']['Twitter'],
                    'image': content['Image']['Path'],
                    'alt': content['Image']['AltText'],
                    'header': '',
                    'body': '',
                    'footer': '',
                    'background': content['Page']['Color']['Background'],
                    'font_color': content['Page']['Color']['Font'],
                    'link': content['Page']['Color']['Clicked-Link'],
                    'font': content['Page']['Font'],
                    'borders': 'none'}

    # Grab the header(s).
    for title in content['Header']:
        site_content['header'] += '<p>' + content['Header'][title] + '</p>'

    # Grab the link(s).
    for link in content['Body']:
        site_content['body'] += '<a target="_blank" href="' + \
                                content['Body'][link] + '">' + link + '</a><br>'

    # Grab the footer(s).
    count = 1
    for title in content['Footer']:
        if title not in ('Copyright', 'CombinedTitle'):
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

    # Set/unset the div borders (good for troubleshooting).
    if content['Page']['Borders']:
        site_content['borders'] = '2px solid yellow'

    # Build Google Analytics.
    build_analytics_object(content, site_content)

    return site_content


def build_resume_object():
    """Convert resume.yaml into a dictionary."""
    with open(RESUME_YAML, encoding='UTF-8') as file:
        content = yaml.safe_load(file)

    # Grab the meta, Overview, & Summary info.
    resume_content = {'author': content['meta']['siteAuthor'],
                      'description': content['meta']['siteDescription'],
                      'icon': content['meta']['siteIcon'],
                      'thumbnail': content['meta']['siteThumbnail'],
                      'tags': ','.join(list(content['meta']['siteTags'])),
                      'twitter': content['meta']['siteTwitter'],
                      'name': content['basics']['name'],
                      'title': content['basics']['label'],
                      'phone': content['basics']['phone'],
                      'email': content['basics']['email'],
                      'subject': content['meta'].get('emailSubject') or '',
                      'summary': content['basics']['summary'],
                      'skills': '',
                      'experience': '',
                      'education': '', }

    # Build the Google Analytics object.
    build_analytics_object(content, resume_content)

    # Skills
    rows = [len(content['Skills'][column]) for column in content['Skills']]
    rows = max(rows)

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
    for exp in content['Experience']:
        resume_content['experience'] += '<div class="job"><h2>' + \
                                        content['Experience'][exp]['Company'] + '</h2><h3>' + \
                                        content['Experience'][exp]['Title'] + '</h3><h4>' + \
                                        content['Experience'][exp]['Dates'] + '</h4>' + '<p>• ' + \
                                        '</p><p>• ' \
                                            .join(list(content['Experience'][exp]['Summary'])) \
                                        + '</p></div>'

    # Certifications
    get_certifications(content, resume_content)

    # Education
    for school in content['education']:
        resume_content['education'] += '<h2>' + school['institution'] + ' - ' + \
                                       school['location'] + '</h2><h3>' + \
                                       school['studyType'] + ' in ' + school['area']
        if 'score' in school:
            resume_content['education'] += ' &mdash; <strong>' + school['score'] \
                                           + ' GPA</strong></h3>'
        else:
            resume_content['education'] += '</h3>'
        if 'courses' in school:
            resume_content['education'] += '<p>• ' + '</p><p>• '. \
                join(list(school['courses'])) + '</p>'

    return resume_content


def get_certifications(config_file, resume_content):
    """Build the certifications object."""

    if not config_file.get('Certifications'):
        resume_content['certifications'] = ''
        return

    cert_count = len(config_file['Certifications'])
    count = 1

    resume_content['certifications'] = '<div class="yui-gf"><div class="yui-u first">' \
                                       '<h2>Certifications</h2></div>' \
                                       '<div class="yui-u"><ul class="talent">'
    for cert in config_file['Certifications']:
        if count < cert_count:
            resume_content['certifications'] += '<li>' + \
                                                config_file['Certifications'][cert]['Title'] + \
                                                '</li>'
        else:
            resume_content['certifications'] += '<li class="last">' + \
                                                config_file['Certifications'][cert]['Title'] + \
                                                '</li>'
        count += 1
    resume_content['certifications'] += '</ul>'

    count = 1
    resume_content['certifications'] += '<ul class="talent-center">'
    for cert in config_file['Certifications']:
        if count < cert_count:
            resume_content['certifications'] += '<li>' + \
                                                config_file['Certifications'][cert]['Year'] + \
                                                '</li>'
        else:
            resume_content['certifications'] += '<li class="last">' + \
                                                config_file['Certifications'][cert]['Year'] + \
                                                '</li>'
        count += 1
    resume_content['certifications'] += '</ul>'

    count = 1
    resume_content['certifications'] += '<ul class="talent">'
    for cert in config_file['Certifications']:
        if count < cert_count:
            resume_content['certifications'] += '<li>' + \
                                                config_file['Certifications'][cert]['License'] + \
                                                '</li>'
        else:
            resume_content['certifications'] += '<li class="last">' + \
                                                config_file['Certifications'][cert]['License'] + \
                                                '</li>'
        count += 1
    resume_content['certifications'] += '</ul></div></div><!--// .yui-gf-->'


def build_analytics_object(config_file, content_object):
    """Build Google Analytics and append to the dictionary."""
    content_object['google_id'] = config_file["meta"].get("googleAnalytics")
    if content_object['google_id']:
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
        "meta": {
            "Author": str,
            "Description": str,
            "Icon": str,
            "Twitter": str,
            "Tags": list,
            schema.Optional("googleAnalytics"): schema.Or(str, None)
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
        "meta": {
            "siteAuthor": str,
            "siteDescription": str,
            "siteIcon": str,
            "siteThumbnail": str,
            "siteTwitter": str,
            "siteTags": list,
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
        schema.Optional("Certifications"): {
            1: {
                "Title": str,
                "Year": str,
                "License": str,
            },
        },
        "education": list
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


def generate_json():
    """Generate a JSON copy of the resume."""
    print("Generating the JSON version of the resume.")
    with open(RESUME_YAML, encoding='UTF-8') as file:
        content = yaml.safe_load(file)

    with open(RESUME_JSON, 'w', encoding='UTF-8') as file:
        json.dump(content, file, indent=2)


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
    job_options.add_argument('-j',
                             '--json',
                             default=False,
                             dest="json_resume",
                             action='store_true',
                             help='Generate the JSON resume copy.')
    job_options.add_argument('-c',
                             '--check',
                             default=False,
                             action='store_true',
                             help='Validate the yaml schema (must include -r or -i).')

    args = job_options.parse_args()

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

    if args.check and args.index and args.resume:
        index_schema()
        resume_schema()
        sys.exit(0)
    elif args.check and args.index:
        index_schema()
        sys.exit(0)
    elif args.check and args.resume:
        resume_schema()
        sys.exit(0)
    elif args.check:
        print('Must specify either -i and/or -r in order to validate the correct schema.')
        sys.exit(1)

    if args.backup and args.index and args.resume:
        backup_files(index_templates)
        backup_files(resume_templates)
    elif args.backup and args.index:
        backup_files(index_templates)
    elif args.backup and args.resume:
        backup_files(resume_templates)
    elif args.backup:
        print('Must specify either -i and/or -r to backup the proper files.')
        sys.exit(1)

    if args.index:
        index_schema()
        site_content = build_index_object()
        update_content(index_templates, site_content, args.stdout)
    if args.resume:
        resume_schema()
        resume_content = build_resume_object()
        update_content(resume_templates, resume_content, args.stdout)
    if args.json_resume:
        generate_json()


if __name__ == "__main__":
    main()
