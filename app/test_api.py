import os
import re
import requests
from dotenv import load_dotenv
from datetime import datetime
from pathlib import Path


# Load environment variables from .env file
# So that we can use them in our code without hardcoding sensitive information
load_dotenv()

MOODLE_URL = os.getenv("MOODLE_URL")
TOKEN = os.getenv("MOODLE_TOKEN")

# This is the main endpoint for Moodle's web service API
# Through this endpoint (URL) we can make requests to various Moodle functions
url = f"{MOODLE_URL}/webservice/rest/server.php"


def sanitize_filename(filename):
    # This function is used to sanitize filenames by removing any characters that are not allowed in filenames
    # The regular expression pattern r'[<>:"/\\|?*]' matches any of the characters < > : " / \ | ? *
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

# These parameters are required for making a request to Moodle's web service API
params = {
    # The 'wstoken' parameter is used to authenticate the request
    "wstoken": TOKEN,

    # The wsfunction parameter specifies which Moodle function we want to call
    "wsfunction": "core_webservice_get_site_info",

    # The moodlewsrestformat parameter specifies the format of the response
    "moodlewsrestformat": "json"

}

# We use the requests library to make a GET request to the Moodle API endpoint

response = requests.get(url, params=params)

# HTTP status code 200 means the request was successful
print("Status Code: ", response.status_code)

# The response from the Moodle API is in JSON format, so we can parse it using the .json() method
site_info = response.json()

print("Antwort:")

# We receive a dictionary from the Moodle API, which contains various information about the site and the user
user_id = site_info["userid"]
fullname = site_info["fullname"]

# We use the user_id to make another request to get the courses that the user is enrolled in

params = {
    "wstoken": TOKEN,
    "wsfunction": "core_enrol_get_users_courses",
    "moodlewsrestformat": "json",
    "userid": user_id
}

# New request to get the course information for the user
response = requests.get(url, params=params)
courses = response.json()

print("Meine Moodle-Kurse: ")

# course_id = input("Geben Sie die Kurs-ID ein, um die Teilnehmerliste abzurufen: ")
course_id = 49370

params = {
    "wstoken": TOKEN,
    "wsfunction": "core_course_get_contents",
    "moodlewsrestformat": "json",
    "courseid": course_id
}

response = requests.get(url, params=params)

course_contents = response.json()

print("Kursinhalte: ")

for section in course_contents:
    for module in section["modules"]:

        if module["modname"] == "assign":


            print("\nAbschnitt: ", section["name"])
            print("Aufgabe: ", module["name"], " (", module["modname"], ")")
            print("URL: ", module["url"])

            for date in module.get("dates", []):

                # The timestamp is in Unix time format, which is the number of seconds since January 1, 1970
                timestamp = date["timestamp"]

                # We convert the timestamp to a human-readable date format using datetime.fromtimestamp()
                readable_date = datetime.fromtimestamp(timestamp).strftime("%d.%m.%Y %H:%M")
                print(date["label"], readable_date)


assign_params = {
    "wstoken": TOKEN,
    "wsfunction": "mod_assign_get_assignments",
    "moodlewsrestformat": "json",

}

for index, course in enumerate(courses):
    assign_params[f"courseids[{index}]"] = course["id"]


response = requests.get(url, params=assign_params)

assignments_data = response.json()


def download_assignment_files(assignment, token, course_name):

# We can access the attachments of the first assignment using the "introattachments" key
    attachments = assignment.get("introattachments", [])

    safe_course_name = sanitize_filename(course_name)
    safe_assignment_name = sanitize_filename(assignment["name"])

    # We create a folder structure to save the downloaded files in a directory named "downloads"
    # The folder structure will be: downloads/course_name/assignment_name
    # assignment_folder = (Path("downloads") / course_name / assignment["name"])

    # We use safe_course_name and safe_assignment_name to avoid any issues with invalid characters in folder names

    assignment_folder = (Path("downloads") / safe_course_name / safe_assignment_name)

    # Create a directory to save the downloaded files if it doesn't exist
    # The mkdir() method creates the directory, and the parents=True argument allows creating parent directories if they don't exist
    # The exist_ok=True argument prevents raising an error if the directory already exists
    assignment_folder.mkdir(parents=True, exist_ok=True)

    for file in attachments:

        filename = file["filename"]
        file_url = file["fileurl"]

        # Download the file using the requests library and the file URL
        download_response = requests.get(
            file_url, params={"token": TOKEN})

        # print("Download Status Code: ", download_response.status_code)

        if download_response.status_code == 200:
            file_path = assignment_folder / filename

            # Save the file to the local filesystem
            with open(file_path, "wb") as f:
                f.write(download_response.content)

            print("Heruntergeladene Datei: ", file_path)
        else:
            print(
                f"Fehler beim Herunterladen der Datei {filename}. Status Code: {download_response.status_code}")

for course in assignments_data["courses"]:
    course_name = course["fullname"]

    for assignment in course["assignments"]:
        download_assignment_files(
            assignment,
            TOKEN,
            course_name
        )

