"""
Build object for web tracking.
"""

from string import Template

# pylint: disable=too-few-public-methods
class Analytics:
    """Analytics operations."""

    @staticmethod
    def build_analytics(config_file, content_object):
        """Build Google Analytics and append to the dictionary."""

        # pylint: disable=unsubscriptable-object
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
