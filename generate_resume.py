#!/usr/bin/env python3

import os
import yaml
from string import Template

def build_resume_object():
    """Convert resume.yaml into a dictionary."""

    with open('resume.yaml') as f:
        content = yaml.safe_load(f)

    resume_content = {}
    ## Grab the meta content.
    resume_content['author']      = content['Meta']['Author']
    resume_content['description'] = content['Meta']['Description']
    resume_content['icon']        = content['Meta']['Icon']
    resume_content['thumbnail']   = content['Meta']['Thumbnail']
    resume_content['tags']        = ','.join([tag for tag in content['Meta']['Tags']])
    resume_content['twitter']     = content['Meta']['Twitter']

    # Build the Google Analytics object.
    if content['Google']['Analytics']:
        resume_content['google_id'] = content['Google']['ID']
        resume_content['google']    = """
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=$google_id"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());

      gtag('config', '$google_id');
    </script>"""

        resume_content['google'] = Template(resume_content['google'])
        resume_content['google'] = resume_content['google'].substitute(resume_content)

    ### Build the resume objects.
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
        resume_content['experience'] += '<div class="job"><h2>' + content['Experience'][xp]['Company'] + '</h2><h3>' + content['Experience'][xp]['Title'] + '</h3><h4>' + content['Experience'][xp]['Dates'] + '</h4>' + '<p>• ' + '</p><p>• '.join([tag for tag in content['Experience'][xp]['Summary']])  + '</p></div>'

    # Certitifications
    CERT_COUNT = len(content['Certifications'])

    count = 1
    resume_content['certifications'] = '<ul class="talent">'
    for cert in content['Certifications']:
        if count < CERT_COUNT:
            resume_content['certifications'] += '<li>' + content['Certifications'][cert]['Title'] + '</li>'
        else:
            resume_content['certifications'] += '<li class="last">' + content['Certifications'][cert]['Title'] + '</li>'
        count += 1
    resume_content['certifications'] += '</ul>'

    count = 1
    resume_content['certifications'] += '<ul class="talent">'
    for cert in content['Certifications']:
        if count < CERT_COUNT:
            resume_content['certifications'] += '<li>' + content['Certifications'][cert]['Year'] + '</li>'
        else:
            resume_content['certifications'] += '<li class="last">' + content['Certifications'][cert]['Year'] + '</li>'
        count += 1
    resume_content['certifications'] += '</ul>'

    count = 1
    resume_content['certifications'] += '<ul class="talent">'
    for cert in content['Certifications']:
        if count < CERT_COUNT:
            resume_content['certifications'] += '<li>' + content['Certifications'][cert]['License'] + '</li>'
        else:
            resume_content['certifications'] += '<li class="last">' + content['Certifications'][cert]['License'] + '</li>'
        count += 1
    resume_content['certifications'] += '</ul>'

    # Education
    print(resume_content)

    return resume_content

def build_resume(source, destination, resume_content, generate):
    """Generate HTML/CSS assets from their templates."""

    if generate:
        if os.path.exists(destination):
            os.remove(destination)
    with open(source, 'r') as f:
        src    = Template(f.read())
        result = src.substitute(resume_content)
    if generate:
        with open(destination, 'a+') as d:
            d.write(result)
    else:
        print(result)
    return


resume_content = build_resume_object()

source      = 'templates/srt-resume.tmpl'
destination = 'srt-resume-yaml.html'
generate    = True

build_resume(source, destination, resume_content, generate)
