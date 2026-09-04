"""
Miscellaneous helper functions required by Alea.
"""

from shutil import copyfile
from pathlib import Path

from datetime import datetime
from zoneinfo import ZoneInfo

import os
import sys
import yaml

class AleaHelperFunctions:
    """Helper functions."""

    @staticmethod
    def read_build_info(build_data_file):
        """Read build information from an optional metadata file."""

        metadata_file = Path(build_data_file)

        if not metadata_file.is_file():
            return None

        build_data = {}

        with metadata_file.open(encoding="UTF-8") as file:
            build_data = yaml.safe_load(file)

        return {"meta": {"buildData": build_data}}

    @staticmethod
    def backup_files(templates):
        """Backup artifacts."""

        for _, paths in templates.items():
            src  = paths["destination"]
            dest = f'{paths["destination"]}.bak'
            print(f'Backing up file: {src}')

            try:
                copyfile(src, dest)
            except OSError:
                print(f'Unable to openfile: {src}')
                sys.exit(5)

    @staticmethod
    def format_date():
        """Format date."""

        central_time = datetime.now(
            ZoneInfo("America/Chicago")
        )

        date = central_time.strftime(
            "%Y-%m-%d %I:%M:%S %p %Z"
        )

        return date

    def get_build_metadata(self):
        """Return GitHub Actions build metadata in the canonical format:
                "meta": {
                    "buildData": {
                        "Build": "...",
                        "Run ID": "...",
                        "Attempt": "...",
                        "Commit": "...",
                        "Date": "..."
                    }
                }
        """

        environment_variables = {
            "Build": "GITHUB_RUN_NUMBER",
            "Run ID": "GITHUB_RUN_ID",
            "Attempt": "GITHUB_RUN_ATTEMPT",
            "Commit": "GITHUB_SHA",
        }

        missing_variables = [
            variable
            for variable in environment_variables.values()
            if not os.getenv(variable)
        ]

        if missing_variables:
            print("[i] Not running in the GitHub Actions build environment.")
            return None

        build_data = {
            key: os.environ[variable]
            for key, variable in environment_variables.items()
        }

        build_data['Date'] = self.format_date()

        return {'meta': {'buildDate': build_data}}
