"""
Render PDF resume from canonical data source.

Rendering is done via Docker and chrome-headless
to ensure consistency with the HTML version.
"""

import subprocess

# pylint: disable=too-few-public-methods
class RenderPdf:
    """Render PDF resume."""

    @staticmethod
    def _run_docker(project_directory):
        """Build the docker-compose command."""
        command = [
            "docker",
            "compose",
            "--project-directory",
            ".",
            "--env-file",
            f"{project_directory}/.env",
            "--file",
            f"{project_directory}/docker-compose.yml",
            "up",
            "--build"
        ]

        print("[+] Starting the PDF rendering environment.")
        print("[i] This may take a moment...")

        try:
            subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            )
        except subprocess.CalledProcessError as error:
            print("[!] PDF generation failed.")
            print(error.stdout)
            print(error.stderr)
            raise

    def render(self, project_directory):
        """Generate a PDF copy of the resume."""
        self._run_docker(project_directory)
