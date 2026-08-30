import os
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv

from .downloader import download_assignment_files

from .moodle_client import (
    get_site_info,
    get_courses,
    get_assignments
)
# Load environment variables from .env file

load_dotenv()

MOODLE_URL = os.getenv("MOODLE_URL")
TOKEN = os.getenv("MOODLE_TOKEN")

url = f"{MOODLE_URL}/webservice/rest/server.php"


app = FastAPI()

# This is the main endpoint for Moodle's web service API
# Through this endpoint (URL) we can make requests to various Moodle functionss

@app.get("/")
def root():
    return {"message": "Moodle Organizer API läuft!"}

# This endpoint retrieves the list of courses for the authenticated user

@app.get("/courses")
def get_user_courses():
    site_info = get_site_info(url, TOKEN)

    user_id = site_info["userid"]

    moodle_courses = get_courses(url, TOKEN, user_id)

    return moodle_courses

@app.get("/courses/{course_id}/assignments")
def course_assignments(course_id: int):
    site_info = get_site_info(url, TOKEN)

    user_id = site_info["userid"]

    moodle_courses = get_courses(url, TOKEN, user_id)

    selected_course = None

    for course in moodle_courses:
        if course["id"] == course_id:
            selected_course = course
            break

    if selected_course is None:
        raise HTTPException(status_code=404, detail="Kurs nicht gefunden :(")
    #     assignments_data
    # → ganze API-Antwort

    # assignments_data["courses"]
    # → Liste der zurückgegebenen Kurse

    # assignments_data["courses"][0]
    # → erster/bei uns einziger Kurs

    # assignments_data["courses"][0]["assignments"]
    # → Aufgaben dieses Kurses

    assignments_data = get_assignments(url, TOKEN, [selected_course])

    # If there are no courses in the assignments_data, return an empty list
    if not assignments_data["courses"]:
        return []

    return assignments_data["courses"][0]["assignments"]

@app.post("/sync")
def sync_moodle():
    site_info = get_site_info(url, TOKEN)

    user_id = site_info["userid"]

    moodle_courses = get_courses(url, TOKEN, user_id)

    assignments_data = get_assignments(url, TOKEN, moodle_courses)


    downloaded_courses = 0
    processed_assignments = 0
    file_downloaded = 0
    file_skipped = 0

    # Loop through each course and its assignments, downloading files for each assignment

    for course in assignments_data["courses"]:
        course_name = course["fullname"]

        downloaded_courses += 1

        for assignment in course["assignments"]:
            processed_assignments += 1

            downloaded, skipped =download_assignment_files(assignment, TOKEN, course_name)

            files_downloaded += downloaded
            files_skipped += skipped

    return {
        "message": "Synchronisierung abgeschlossen!",
        "downloaded_courses": downloaded_courses,
        "assignments_processed": processed_assignments,
        "files_downloaded": files_downloaded,
        "files_already_existing": files_skipped
    }