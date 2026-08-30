import re
import os
import requests


from pathlib import Path


def sanitize_filename(filename):
    # This function is used to sanitize filenames by removing any characters that are not allowed in filenames
    # The regular expression pattern r'[<>:"/\\|?*]' matches any of the characters < > : " / \ | ? *
    return re.sub(r'[<>:"/\\|?*]', '_', filename)


# This function is used to download assignment files from Moodle

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


    downloaded = 0
    skipped = 0

    for file in attachments:

        filename = file["filename"]
        file_url = file["fileurl"]

        file_path = assignment_folder / filename

        if file_path.exists():
            # If the file already exists, we skip downloading it and print a message indicating that the file is being skipped
            skipped += 1
            continue

        # Download the file using the requests library and the file URL
        download_response = requests.get(
            file_url, params={"token": token})

        # print("Download Status Code: ", download_response.status_code)

        if download_response.status_code == 200:

            # Save the file to the local filesystem
            with open(file_path, "wb") as f:
                f.write(download_response.content)

            downloaded += 1

    return downloaded, skipped
        
        # else:
        #     print(
        #         f"Fehler beim Herunterladen der Datei {filename}. Status Code: {download_response.status_code}")



