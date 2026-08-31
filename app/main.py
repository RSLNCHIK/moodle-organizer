# CLI-/Skript-Einstiegspunkt
# This file serves as the entry point for the command-line interface (CLI) or script execution. It is responsible for initializing the application, loading environment variables, and orchestrating the main workflow of the application.

import os

from dotenv import load_dotenv

from .moodle_client import (
    get_site_info,
    get_courses,
    get_assignments
)


from .downloader import download_assignment_files

# Load environment variables from .env file
# So that we can use them in our code without hardcoding sensitive information
load_dotenv()


MOODLE_URL = os.getenv("MOODLE_URL")
TOKEN = os.getenv("MOODLE_TOKEN")


# This is the main endpoint for Moodle's web service API
# Through this endpoint (URL) we can make requests to various Moodle functions
url = f"{MOODLE_URL}/webservice/rest/server.php"


site_info = get_site_info(url, TOKEN)

user_id = site_info["userid"]
fullname = site_info["fullname"]

print("Angemeldet als: ", fullname)


courses = get_courses(url, TOKEN, user_id)

print("\nMeine Kurse: ")

for course in courses:
    print(course["id"], "-", course["fullname"])


assignments_data = get_assignments(url, TOKEN, courses)

for course in assignments_data["courses"]:
    course_name = course["fullname"]
    print(f"\n{course_name}:")

    for assignment in course["assignments"]:
        download_assignment_files(assignment, TOKEN, course_name)

