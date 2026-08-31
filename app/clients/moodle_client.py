import requests


# This function is used to get site information from Moodle's web service API

def get_site_info(_url, token):
    params = {
        "wstoken": token,
        "wsfunction": "core_webservice_get_site_info",
        "moodlewsrestformat": "json"
    }

    print(f"Sending request to: {_url}")

    response = requests.get(_url, params=params)

    return response.json()


# This function is used to get the courses that a user is enrolled in from Moodle's web service API

def get_courses(_url, token, user_id):
    params = {
        "wstoken": token,
        "wsfunction": "core_enrol_get_users_courses",
        "moodlewsrestformat":"json",
        "userid": user_id
    }

    response = requests.get(_url, params=params)

    return response.json()

# This function is used to get the assignments for a list of courses from Moodle's web service API

def get_assignments(_url, token, courses):
    params = {
        "wstoken": token,
        "wsfunction": "mod_assign_get_assignments",
        "moodlewsrestformat": "json"
    }

    for index, course in enumerate(courses):
        params[f"courseids[{index}]"] = course["id"]

    response = requests.get(_url, params=params)

    return response.json()

    

