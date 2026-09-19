import requests
from typing import Any


class MoodleAPIError(Exception):
    def __init__(self, message: str, error_code: str | None = None):
        self.message = message
        self.error_code = error_code
        # Call the base class constructor with the parameters it needs
        super().__init__(message)

def build_api_url(base_url):
    # rstrip any trailing slashes from the base URL to avoid double slashes in the final URL
    base_url = base_url.rstrip('/')

    if base_url.endswith("webservice/rest/server.php"):
        return base_url

    return f"{base_url}/webservice/rest/server.php"

# This function is used to get site information from Moodle's web service API

def get_site_info(base_url: str, token: str)-> dict[str, Any]:
    params = {
        "wstoken": token,
        "wsfunction": "core_webservice_get_site_info",
        "moodlewsrestformat": "json"
    }


    data = moodle_request(base_url, params)

    if not isinstance(data, dict):
        raise MoodleAPIError("Moodle hat beim Abrufen der Site-Informationen ein unerwartetes Fromat zuruckgegeben.")

    return data


def moodle_request(base_url: str, params: dict) -> dict[str, Any] | list[Any]:
    api_url = build_api_url(base_url)

    try:
        response = requests.get(api_url, params=params, timeout=15)
        response.raise_for_status() # Raise an HTTPError for bad requests
    except requests.exceptions.Timeout:
        raise MoodleAPIError("Request timed out")
    except requests.exceptions.HTTPError as http_err:
        raise MoodleAPIError(f"HTTP error occurred: {response.status_code}")
    except requests.exceptions.ConnectionError:
        raise MoodleAPIError("Connection error occured")

    try:
        data = response.json()

    except ValueError:
        raise MoodleAPIError("Die angegebene Adresse scheint keine gültige Moodle-REST-API zu sein.")


    if isinstance(data, dict) and "exception" in data:
        raise MoodleAPIError(
            message=data.get("message", "Moodle API Fehler"),
            error_code=data.get("errorcode"))
    
    return data


# This function is used to get the courses that a user is enrolled in from Moodle's web service API

def get_courses(base_url: str, token: str, moodle_user_id: int) -> list[dict[str, Any]]:
    params = {
        "wstoken": token,
        "wsfunction": "core_enrol_get_users_courses",
        "moodlewsrestformat":"json",
        "userid": moodle_user_id
    }

    data = moodle_request(base_url, params)


    if not isinstance(data, list):
        raise MoodleAPIError("Moodle hat beim Abrufen der Kurse ein unerwartetes Format zurueckgegeben.")

    return data

# This function is used to get the assignments for a list of courses from Moodle's web service API

def get_assignments(base_url: str, token: str, courses: list[dict[str, Any]]) -> dict[str, Any]:
    params = {
        "wstoken": token,
        "wsfunction": "mod_assign_get_assignments",
        "moodlewsrestformat": "json"
    }

    for index, course in enumerate(courses):
        params[f"courseids[{index}]"] = course["id"]

    data = moodle_request(base_url, params)

    if not isinstance(data, dict):
        raise MoodleAPIError("Moodle hat beim Abrufen der Aufgaben ein unerwartetes Format zuruckgegeben.")
    
    return data