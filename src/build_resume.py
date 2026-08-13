"""
Build resume object.
"""

from datetime import datetime

import numpy
import yaml

from .analytics import Analytics
from .schema import SchemaValidations

class BuildResume:
    """Resume operations."""

    RESUME_YAML = 'configs/resume.yaml'
    RESUME_JSON = 'resumes/resume.json'

    def build_resume_object(self) -> dict:
        """Convert resume.yaml into a dictionary."""

        # Validate Schema.
        SchemaValidations.resume_schema()

        with open(self.RESUME_YAML, encoding='UTF-8') as file:
            content = yaml.safe_load(file)

        # Grab the meta, Overview, & Summary info.
        resume_content = {'author': content['meta']['siteAuthor'],
                        'description': content['meta']['siteDescription'],
                        'icon': content['meta']['siteIcon'],
                        'thumbnail': content['meta']['siteThumbnail'],
                        'tags': ','.join(list(content['meta']['siteTags'])),
                        'name': content['basics']['name'],
                        'title': content['basics']['label'],
                        'phone': content['basics']['phone'],
                        'email': content['basics']['email'],
                        'subject': content['meta'].get('emailSubject') or '',
                        'summary': content['basics']['summary'],
                        'skills': '',
                        'experience': '',
                        'education': '',
                        'publications': '',
                        'volunteer': '', }

        # Build the Google Analytics object.
        Analytics.build_analytics(content, resume_content)

        # Skills
        skills = []
        for section in content['skills']:
            for skill in section['keywords']:
                skills.append(skill)
        rows = numpy.array_split(skills, 3)
        skill_lists = [len(row) for row in rows]
        longest_list = max(skill_lists)

        for row in rows:
            resume_content['skills'] += '<ul class="talent">'
            count = 0
            for skill in row:
                count += 1
                if count == longest_list:
                    resume_content['skills'] += '<li class="last">' + skill + "</li>"
                else:
                    resume_content['skills'] += "<li>" + skill + "</li>"
            resume_content['skills'] += "</ul>"

        # Experience
        BuildResume.get_experience(content, resume_content)

        # Certifications
        BuildResume.get_certifications(content, resume_content)

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

        # Publications
        BuildResume.get_publications(content, resume_content)

        # Volunteer Work
        BuildResume.get_volunteer_work(content, resume_content)

        return resume_content

    @staticmethod
    def get_experience(config_file, resume_content):
        """Build the experience object."""

        # pylint: disable=unsubscriptable-object
        for experience in config_file['work']:
            start_year = int(experience["startDate"].split("-")[0])
            start_month = int(experience["startDate"].split("-")[1])
            start_day = int(experience["startDate"].split("-")[2])
            start = datetime(start_year, start_month, start_day)
            start_month = start.strftime("%B")
            end_year = int(experience["endDate"].split("-")[0])
            end_month = int(experience["endDate"].split("-")[1])
            end_day = int(experience["endDate"].split("-")[2])
            end = datetime(end_year, end_month, end_day)
            end_month = end.strftime("%B")
            start = f"{start_month} {start_year}"
            end = f"{end_month} {end_year}"

            if experience.get("currentEmployee"):
                end = "Present"

            resume_content['experience'] += '<div class="job"><h2>' + \
                                            experience['name'] + '</h2><h3>' + \
                                            experience['position'] + '</h3><h4>' + \
                                            start + '-' + end + '</h4>' + '<p>• ' + \
                                            '</p><p>• '.join(experience['highlights']) \
                                            + '</p></div>'

    @staticmethod
    def get_certifications(config_file, resume_content):
        """Build the certifications object."""

        # pylint: disable=no-member
        if not config_file.get('certificates'):
            resume_content['certifications'] = ''
            return

        # pylint: disable=unsubscriptable-object
        cert_count = len(config_file['certificates'])
        count = 1

        # pylint: disable=unsubscriptable-object
        resume_content['certifications'] = '<div class="yui-gf"><div class="yui-u first">' \
                                        '<h2>Certifications</h2></div>' \
                                        '<div class="yui-u"><ul class="talent">'
        for cert in config_file['certificates']:
            if count < cert_count:
                resume_content['certifications'] += '<li>' + \
                                                    cert['issuer'] + ' ' + cert['name'] + \
                                                    '</li>'
            else:
                resume_content['certifications'] += '<li class="last">' + \
                                                    cert['issuer'] + ' ' + cert['name'] + \
                                                    '</li>'
            count += 1
        resume_content['certifications'] += '</ul>'

        count = 1
        resume_content['certifications'] += '<ul class="talent-center">'
        # pylint: disable=unsubscriptable-object
        for cert in config_file['certificates']:
            year = cert['date'].split("-")
            if count < cert_count:
                resume_content['certifications'] += '<li>' + year[0] + '</li>'
            else:
                resume_content['certifications'] += '<li class="last">' + year[0] + '</li>'
            count += 1
        resume_content['certifications'] += '</ul>'

        count = 1
        resume_content['certifications'] += '<ul class="talent">'
        # pylint: disable=unsubscriptable-object
        for cert in config_file['certificates']:
            if count < cert_count:
                resume_content['certifications'] += '<li>' + \
                                                    cert['license'] + \
                                                    '</li>'
            else:
                resume_content['certifications'] += '<li class="last">' + \
                                                    cert['license'] + \
                                                    '</li>'
            count += 1
        resume_content['certifications'] += '</ul></div></div><!--// .yui-gf-->'

    @staticmethod
    def get_publications(config_file, resume_content):
        """Build the publications object."""

        count      = 1
        # pylint: disable=unsubscriptable-object
        name       = config_file['basics']['name'].split()
        last_name  = name[1]
        first_name = name[0]

        for publication in config_file['publications']:
            release_year = int(publication["releaseDate"].split("-")[0])
            release_month = int(publication["releaseDate"].split("-")[1])
            release_day = int(publication["releaseDate"].split("-")[2])
            release_date = datetime(release_year, release_month, release_day)
            release_month = release_date.strftime("%B")
            release = f"{release_month} {release_day}, {release_year}"
            resume_content['publications'] += '<p><strong>' + str(count) + \
                                            '.</strong>    ' + last_name + ', ' + \
                                            first_name + ' (' + str(release) + '). ' + \
                                            '<a href="' + publication["url"] + '">' + \
                                            publication["name"] + '.</a> ' + \
                                            publication["publisher"] + '.</p>'
            count += 1

    @staticmethod
    # pylint: disable=unsubscriptable-object
    def get_volunteer_work(config_file, resume_content):
        """Build the volunteer_work object."""

        # pylint: disable=unsubscriptable-object
        for work in config_file['volunteer']:
            start_year = int(work["startDate"].split("-")[0])
            start_month = int(work["startDate"].split("-")[1])
            start_day = int(work["startDate"].split("-")[2])
            start = datetime(start_year, start_month, start_day)
            start_month = start.strftime("%B")
            end_year = int(work["endDate"].split("-")[0])
            end_month = int(work["endDate"].split("-")[1])
            end_day = int(work["endDate"].split("-")[2])
            end = datetime(end_year, end_month, end_day)
            end_month = end.strftime("%B")
            start = f"{start_month} {start_year}"
            end = f"{end_month} {end_year}"

            if work.get("current"):
                end = "Present"

            resume_content['volunteer'] += '<div class="job"><h2>' + \
                                            work['organization'] + '</h2><h3>' + \
                                            work['position'] + '</h3><h4>' + \
                                            start + '-' + end + '</h4>' + '<p>• ' + \
                                            '</p><p>• '.join(work['highlights']) \
                                            + '</p></div>'
